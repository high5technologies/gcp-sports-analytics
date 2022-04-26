import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
from bs4 import BeautifulSoup, Comment
import urllib.request

def nba_espn_worker_individual_playbyplay_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        game_date = message_data['game_date']
        espn_key = message_data['espn_key']
        away_abbrev = message_data['away_abbrev']
        home_abbrev = message_data['home_abbrev']
        start_time = message_data['start_time']
       
        url = "https://www.espn.com/nba/playbyplay/_/gameId/" + str(espn_key)
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        quarters = soup.find(id="gamepackage-qtrs-wrap").find_all('table')

        plays = []
        quarter_number = 1
        play_number = 1
        for quarter in quarters:
            #rows = soup.find_all('table', {"cellspacing": "5"}).find_all('tr')
            rows = quarter.find_all('tr')
            for row in rows:
                if len(row.find_all('td')) > 0:
                    play = {}
                    play['espn_key'] = espn_key
                    play['game_date'] = game_date
                    play['away_abbrev'] = away_abbrev
                    play['home_abbrev'] = home_abbrev
                    play['start_time'] = start_time
                    play['quarter_number'] = quarter_number
                    play['play_number'] = play_number
                    play['time_stamp'] = get_text(row.find_all('td', {'class':'time-stamp'})[0])
                    play['team_logo_url'] = row.find_all('td', {'class':'logo'})[0].find('img')['src']
                    
                    if play['team_logo_url'].replace('https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/','').find(away_abbrev.lower()) >= 0:
                        play['play_h_a'] = 'A'
                        play['play_team_abbrev'] = away_abbrev
                    elif play['team_logo_url'].replace('https://a.espncdn.com/combiner/i?img=/i/teamlogos/nba/500/','').find(home_abbrev.lower()) >= 0:
                        play['play_h_a'] = 'H'
                        play['play_team_abbrev'] = home_abbrev
                    play['game_details'] = get_text(row.find_all('td', {'class':'game-details'})[0])
                    play['combined_score_a_h'] = get_text(row.find_all('td', {'class':'combined-score'})[0])
                    play["play_key"] = str(play['espn_key']) + '|' + str(play['play_number'])
                    play["load_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    plays.append(play)
                    play_number += 1
            #soup.find_all(class_="Bob")
            #print(quarter_number)
            quarter_number += 1

        #print(plays)            
        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_espn_playbyplay'
        replication_data['data'] = plays
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        return f'ESPN Play by Play successfully scraped'

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

def get_text(stat):
    if stat is not None:
        txt = stat.text.replace("^","").replace("\xa0","").strip()
        if txt == "":
            txt = None
    else:
        txt = None
    return txt