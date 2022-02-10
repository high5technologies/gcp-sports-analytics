import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import urllib.request

def ahl_roster_season_scraper(event, context):
    
    # Config
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

        season = message_data['season']
        docs = fs.collection(u'reference').document(u'AHL').collection('ahl_hockeytech_seasons').where(u'season',u'==',str(season)).stream()
            
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
                    if dt >= season_start_date and dt <= season_end_date and season_index not in season_indexes:
                        season_indexes.append(season_index)

        if not season_indexes:
            raise ValueError("season config does not exist in firestore reference.AHL.ahl_hockeytech_season")

        # loop through seasons that matched search criteria from firestore (reg season and playoffs are 2 separate season_indexes)
        for season_index in season_indexes:
    
            url = "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=bootstrap&season=" + season_index + "&pageName=roster&key=50c2cd9b5e18e390&client_code=ahl&lang=en"
            response = requests.get(url) 
            raw_json = json.loads(response.text[1:-1])
            for team in raw_json["teams"]:
                g = {}
                g['season_index'] = season_index
                g['team_id'] = team['id']
                
                data_string = json.dumps(g)  
                topic_id = "ahl_ahlcom_roster_season_teams_to_scrape"
                topic_path = publisher.topic_path(project_id, topic_id)
                future = publisher.publish(topic_path, data_string.encode("utf-8"))  

        return f'HockeyTech Rosters successfully scraped'

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
        
        topic_id_error = "error_log_topic"
        data_string_error = json.dumps(err) 
        topic_path_error = publisher.topic_path(project_id, topic_id_error)
        future = publisher.publish(topic_path_error, data_string_error.encode("utf-8"))
        
        
        
