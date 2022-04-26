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

def nba_nbacom_worker_Schedule_scraper(event, context):
    
    # Config
    project_id = os.environ.get('GCP_PROJECT')
    topic_id = "nba_nbacom_games_to_scrape"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        date_string = message_data['date_string']
        date_formatted = message_data['date_formatted']

        url = "https://www.nba.com/games?date=" + date_formatted
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')

        script = soup.find("script", {"id": "__NEXT_DATA__"})
        data = json.loads(script.string)
        
        for game in data['props']['pageProps']['games']:
            game_id = game['gameId']
            home_team = game['homeTeam']['teamTricode'].lower()
            away_team = game['awayTeam']['teamTricode'].lower()
            url_id = away_team + '-vs-' + home_team + '-' + game_id
            gs = {}
            gs['game_date'] = date_formatted
            gs['url_id'] = url_id
            
            data_string = json.dumps(gs)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        return f'NBA.com schedule successfully scraped'


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

            