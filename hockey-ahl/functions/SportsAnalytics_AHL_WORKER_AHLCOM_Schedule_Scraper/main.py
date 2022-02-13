import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
#from bs4 import BeautifulSoup, Comment
import urllib.request

# This scrapes the AHL schedule for a single month
# There may be multiple season_indexes .. for example, scraping April will find the season_index for both reg season & playoffs


def ahl_ahlcom_worker_schedule_scraper(event, context):
    
    # Config
    #project_id = os.environ.get('GCP_PROJECT')
    #topic_id = "nba_nbacom_games_to_scrape"
    #publisher = pubsub_v1.PublisherClient()
    #topic_path = publisher.topic_path(project_id, topic_id)
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    fs = firestore.Client()

    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
        print(message_data)

        monthname = message_data['monthname']
        month = message_data['month_number']
        year = message_data['year']
        season = message_data['season']
        rerun = message_data['rerun']
        start_date = datetime.strptime(message_data['start_date'], '%Y-%m-%d').date()  
        end_date = datetime.strptime(message_data['end_date'], '%Y-%m-%d').date()  

        # Get list of dates in month
        delta = end_date - start_date       # as timedelta

        dates_to_scrape = []
        scrape_flag = False  #reset check flag
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            dt = day.strftime("%Y-%m-%d")
            #print(dt)
            col_ref_key = str(dt) 
            docs = fs.collection(u'AHL').document(u'schedule').collection(col_ref_key).stream()
            
            cnt = 0
            for doc in docs:
                #print(f'{doc.id} => {doc.to_dict()}')
                doc_schedule = doc.to_dict()
                #firestore_schedule.append(doc_schedule)
                cnt += 1
                if "FINAL" not in doc_schedule['game_status'].upper():
                    scrape_flag = True
            if cnt == 0:
                scrape_flag = True # scrape month if nothing in schedule archive

            if scrape_flag or rerun:
                dates_to_scrape.append(dt)
        print(dates_to_scrape)
        #games_to_ignore = []
        #for gm in firestore_schedule:
        #    if "FINAL" in gm['game_status'].upper():
        #        games_to_ignore.append(gm['schedule_key'])

        ##########################################################################
        # Scrape Schedule
        ##########################################################################
    
        if len(dates_to_scrape) > 0:
            
            # Get hockey tech season key from firestore
            docs = fs.collection(u'reference').document(u'AHL').collection(u'ahl_hockeytech_seasons').where(u'season',u'==',str(season)).stream()
            
            season_indexes = []
            for doc in docs:
                d = doc.to_dict()
                event_flag = d['event_flag']
                season_start_date = datetime.strptime(d['start_date'], '%Y-%m-%d').date()
                season_end_date = datetime.strptime(d['end_date'], '%Y-%m-%d').date()
                season_index = d['hockeytech_key']
                
                if not event_flag:
                    for dt_str in dates_to_scrape:
                        dt = datetime.strptime(dt_str, '%Y-%m-%d').date()  
                        #print({"dt":dt,"season_start_date":season_start_date,"season_end_date":season_end_date})
                        if dt >= season_start_date and dt <= season_end_date and season_index not in season_indexes:
                            season_indexes.append(season_index)

            # START HERE ... logic to check for event ... break FOR if event date match, else keep looping ... 
            #{"season":"2014","season_type":"playoff","hockeytech_key":"47"     ,"event_flag":false,"start_date":"","end_date":""}
            #doc_ref_key = str(season) + '_reg'
            #doc_ref = fs.collection(u'reference').document(u'AHL').collection('ahl_hockeytech_seasons').document(doc_ref_key)
            #doc = doc_ref.get()
            
            #if doc.exists:
            #    json_key = doc.to_dict()
            #    season_index = json_key['hockeytech_key']
            #else:
            #    raise ValueError("season config does not exist in firestore reference.AHL.ahl_hockeytech_season")
            if not season_indexes:
                raise ValueError("season config does not exist in firestore reference.AHL.ahl_hockeytech_season")

            # loop through seasons that matched search criteria from firestore (reg season and playoffs are 2 separate season_indexes)
            for season_index in season_indexes:
                
                # Create URL
                url = "http://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=schedule&season=" + str(season_index) + "&month=" + str(month) + "&location=homeaway&key=50c2cd9b5e18e390&client_code=ahl"    
                response = requests.get(url) 
            
                raw_json = json.loads(response.text[1:-1])

                for game in raw_json[0]["sections"][0]["data"]:
                    g = {}
                    g["game_date"] = datetime.strptime(game["row"]["date_with_day"] + " " + str(year), '%a, %b %d %Y').strftime("%Y-%m-%d")
                    #print(datetime.strptime(game["row"]["date_with_day"] + " " + str(v['year']), '%a, %b %d %Y').strftime("%Y-%m-%d"))
                    g["game_id"] = game["row"]["game_id"]
                    g["game_status"] = game["row"]["game_status"]
                    g["home_team_city"] = game["row"]["home_team_city"]
                    g["visiting_team_city"] = game["row"]["visiting_team_city"]
                    g["home_goal_count"] = game["row"]["home_goal_count"]
                    g["visiting_goal_count"] = game["row"]["visiting_goal_count"]
                    g["schedule_key"] = g["game_id"]
                    g['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    
                    if g["game_date"] in dates_to_scrape:
                        #print(g["game_id"])
                        data_string = json.dumps(g)  
                        topic_id = "ahl_ahlcom_games_to_scrape"
                        topic_path = publisher.topic_path(project_id, topic_id)
                        future = publisher.publish(topic_path, data_string.encode("utf-8"))   
                    #dt = datetime.strptime(g["game_date"],"%Y-%m-%d").date()
                    #if dt in >= startDate and dt <= endDate:
                    #    if g["game_id"] not in games_to_ignore or rerun == 'y':
                    #        schedule.append(g)
                        
        #print(schedule) 
        return f'ahl.com schedule successfully scraped'
    except Exception as e:
        err = {}
        err['error_key'] = str(uuid.uuid4())
        err['error_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        err['function'] = os.environ.get('FUNCTION_NAME')
        err['data_identifier'] = "none"
        err['trace_back'] = str(traceback.format_exc())
        err['message'] = str(e)
        #err['data'] = data if data is not None else ""
        print(err)

        # Log error
        topic_id_error = "error_log_topic"
        data_string_error = json.dumps(err) 
        topic_path_error = publisher.topic_path(project_id, topic_id_error)
        future = publisher.publish(topic_path_error, data_string_error.encode("utf-8"))
        
       

        

