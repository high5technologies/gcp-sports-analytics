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
import re 

def nba_espn_worker_individual_gamecast_scraper(event, context):
    
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
       
        url = "https://www.espn.com/nba/game?gameId=" + str(espn_key)
        r = requests.get(url)
        data_list = re.findall("espn.gamepackage.probability.data(.+?);", r.content.decode("utf-8"))
        for data in data_list:
            data = data.replace("espn.gamepackage.probability.data","").strip().replace("=","",1).strip()
            if data[-1] == ";":
                data = data[:-1].strip()
            
            d = json.loads(data)

            game = {}
            game['espn_key'] = espn_key
            game['game_date'] = game_date
            game['away_abbrev'] = away_abbrev
            game['home_abbrev'] = home_abbrev
            game['start_time'] = start_time
            if len(d) > 0:
                game["espn_home_win_perc"] = d[0]["homeWinPercentage"]
            else:
                game["espn_home_win_perc"] = None
            game["load_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            ##########################################################################
            # Publish to BigQuery Replication Topic
            ##########################################################################
            games = []
            games.append(game)

            replication_data = {}
            replication_data['bq_dataset'] = 'nba' 
            replication_data['bq_table'] = 'raw_espn_predictions'
            replication_data['data'] = games
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        return f'ESPN Predictions successfully scraped'

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

            