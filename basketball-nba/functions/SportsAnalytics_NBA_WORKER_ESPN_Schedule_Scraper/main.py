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
import urllib.request
from google.cloud import logging

def nba_espn_worker_Schedule_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()

    topic_id_gamecast = "nba_espn_games_to_scrape_gamecast"
    topic_path_gamecast = publisher.topic_path(project_id, topic_id_gamecast)
    
    topic_id_playbyplay = "nba_espn_games_to_scrape_playbyplay"
    topic_path_playbyplay = publisher.topic_path(project_id, topic_id_playbyplay)

    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)

    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        date_string = message_data['date_string']
        date_formatted = message_data['date_formatted']

        logger.log_text(date_string)

        url = "https://www.espn.com/nba/scoreboard/_/date/" + date_string
        r = requests.get(url)

        games = []
        data_list = re.findall("window.espn.scoreboardData(.+?)window.espn.scoreboardSettings", r.content.decode("utf-8"))
        for data in data_list:
            data = data.replace("window.espn.scoreboardData","").replace("window.espn.scoreboardSettings","").strip().replace("=","",1).strip()[:-1].strip()
            j = json.loads(data)
            #print(j["leagues"][0]["calendarIsWhitelist"])
            for event in j["events"]:
                game = {}
                game["game_date"] = date_formatted
                game["espn_key"] = event["id"]
                short_name = event["shortName"]
                game["away_abbrev"] = short_name.split("@")[0].strip()
                game["home_abbrev"] = short_name.split("@")[1].strip()
                game["start_time"] = event["date"]
                game["load_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                logger.log_text("game_date:"+game["game_date"]+"; espn_key:" + game["espn_key"] + "; away:" + game["away_abbrev"] + "; home:" + game["home_abbrev"])


                if event["status"]["type"]["name"] != "STATUS_POSTPONED":
                    #games.append(game)
                
                    data_string = json.dumps(game)  
                    future = publisher.publish(topic_path_gamecast, data_string.encode("utf-8")) 
                    future = publisher.publish(topic_path_playbyplay, data_string.encode("utf-8")) 

        return f'ESPN schedule successfully scraped'
        
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

            