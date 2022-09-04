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
from google.cloud import logging

def nba_swish_worker_individual_dfssalary_scraper(event, context):

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

        game_date = message_data['date_formatted']
        #game_url_id = message_data['url_id']
        #game_key = message_data['game_key']
        date_string = message_data['date_string']
        #games = message_data['games']

        url = 'https://swishanalytics.com/optimus/nba/daily-fantasy-salary-changes?date=' + str(game_date)
        logger.log_text("url:"+url)

        r = requests.get(url)
        #print(r.content[0:3000])
        page_content = r.content
        soup = BeautifulSoup(page_content, 'html.parser')
        scripts = soup.find_all("script")
        script_with_data = ""
        is_found = False
        for script in scripts:
            if 'this.players_dk' in str(script):
                script_with_data = str(script)
                is_found = True
                break

        #if not is_found:
        #    throw new exception ....

        # Parse HTML to get javascript JSON data objects
        dk_base_index = script_with_data.find("this.players_dk")
        dk_start = script_with_data.find("[",dk_base_index)
        dk_end = script_with_data.find("]",dk_start) + 1
        dk_string = script_with_data[dk_start:dk_end]
        dk_json = json.loads(dk_string)

        fd_base_index = script_with_data.find("this.players_fd")
        fd_start = script_with_data.find("[",fd_base_index)
        fd_end = script_with_data.find("]",fd_start) + 1
        fd_string = script_with_data[fd_start:fd_end]
        fd_json = json.loads(fd_string)

        # Map JSON - specify columns so new columns doesn't break ingestion
        data = []
        for record in dk_json:
            d = {}
            d['player_id'] = record['player_id']
            d['player_name'] = record['player_name']
            d['team_abbr'] = record['nickname']
            d['pos_main'] = record['pos_main']
            d['projected_fantasy_pts'] = record['fantasy_pts']
            d['avg_pts'] = record['avg_pts']
            d['fpts_diff'] = record['fpts_diff']
            d['prev_game_date'] = record['date']
            d['salary'] = record['salary']
            d['salary_diff'] = record['salary_diff']
            d['salary_diff_percentage'] = record['salary_diff_percentage']
            d['game_date'] = game_date
            d['salary_source'] = 'dk'
            d['swish_salary_key'] = str(d['salary_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id'])
            d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            data.append(d)

        for record in fd_json:
            d = {}
            d['player_id'] = record['player_id']
            d['player_name'] = record['player_name']
            d['team_abbr'] = record['nickname']
            d['pos_main'] = record['pos_main']
            d['projected_fantasy_pts'] = record['fantasy_pts']
            d['avg_pts'] = record['avg_pts']
            d['fpts_diff'] = record['fpts_diff']
            d['prev_game_date'] = record['date']
            d['salary'] = record['salary']
            d['salary_diff'] = record['salary_diff']
            d['salary_diff_percentage'] = record['salary_diff_percentage']
            d['game_date'] = game_date
            d['salary_source'] = 'fd'
            d['swish_salary_key'] = str(d['salary_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id'])
            d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            data.append(d)


        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        
        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_swish_salary'
        replication_data['data'] = data
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        
        return f'SwishAnalytics Salaries successfully scraped'

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
