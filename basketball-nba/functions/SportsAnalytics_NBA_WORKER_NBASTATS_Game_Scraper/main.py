import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import urllib.request
from google.cloud import logging
import time

def nba_nbastats_worker_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
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
        season_nbastats = message_data['season_nbastats']
        logger.log_text("date:" + date_formatted + "; season:" + season_nbastats)
        ###########################################################################
        # CODE
        ###########################################################################

        url = 'https://stats.nba.com/stats/leaguegamelog'
        STATS_HEADERS = {
                'Host': 'stats.nba.com',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'x-nba-stats-origin': 'stats',
                'x-nba-stats-token': 'true',
                'Connection': 'keep-alive',
                'Referer': 'https://stats.nba.com/',
                'Pragma': 'no-cache',
                'Cache-Control': 'no-cache',
            }
        static_headers = ['SEASON_ID', 'TEAM_ID', 'TEAM_ABBREVIATION', 'TEAM_NAME', 'GAME_ID', 'GAME_DATE', 'MATCHUP', 'WL', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS', 'PLUS_MINUS', 'VIDEO_AVAILABLE']
        static_name = 'LeagueGameLog'
        season_types = ['Regular Season', 'Playoffs']

        logger.log_text("1")
        found = False
        for season_type in season_types:
            if not found:
                logger.log_text("2")
                payload = {
                    'Counter': '1000',
                    'DateFrom': date_formatted,
                    'DateTo': date_formatted,
                    'Direction': 'DESC',
                    'LeagueID': '00',
                    'PlayerOrTeam': 'T',
                    'Season': season_nbastats,
                    'SeasonType': season_type,
                    'Sorter': 'DATE'}

                #'Season': '', #2014-15
                #'SeasonType': 'Regular Season'
                logger.log_text("3")
                jsonData = requests.get(url, headers=STATS_HEADERS, params=payload, verify=False, timeout=10).json()
                logger.log_text("4")
                data = jsonData['resultSets'][0]
                api_name = data['name']
                headers = data['headers']
                rowSet = data['rowSet']

                logger.log_text("5")
                if api_name != static_name:
                    raise ValueError("static name does not match api")
                if set(headers) != set(static_headers):
                    raise ValueError("headers list does not match")

                load_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                logger.log_text("6")
                d = []
                for row in rowSet:
                    r = {}
                    for i in range(len(headers)):
                        r[headers[i].lower()] = row[i]
                    r['load_datetime'] = load_datetime
                    d.append(r)
                logger.log_text("7")
                logger.log_text("season_type:" + season_type + "; count:" + str(len(d)))
                logger.log_text("8")
                # Check if data returned - loop to try next season_type if no data returned
                if len(d) > 0:
                    found = True
                
                logger.log_text("9")   
        ###########################################################################
        ###########################################################################
        
        logger.log_text("10")

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_nbastats_game'
        replication_data['data'] = d
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   
        
        logger.log_text("11")

        return f'nba stats api schedule successfully scraped'


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

            