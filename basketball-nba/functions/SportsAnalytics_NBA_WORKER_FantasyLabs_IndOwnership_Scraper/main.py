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
from google.cloud import logging


def nba_fantasylabs_worker_individual_ownership_scraper(event, context):

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

        gd = datetime.strptime(game_date, '%Y-%m-%d')
        year = gd.strftime("%Y")
        month = int(gd.strftime("%m"))
        day = int(gd.strftime("%d"))

        url_date = str(month) + '_' + str(day) + '_' + str(year)

        url = 'https://www.fantasylabs.com/api/ownership-contestgroups/2/4/' + url_date + '/'
        logger.log_text("url:"+url)

        r = requests.get(url)
        json_string = r.content
        data_ids = json.loads(json_string)

        data = []

        for group in data_ids:
            draft_group_id = group['DraftGroupId']

            url = 'https://www.fantasylabs.com/api/contest-ownership/2/' + url_date + '/4/' + str(draft_group_id) + '/0/'
            r = requests.get(url)
            json_string = r.content
            data_json = json.loads(json_string)

            for record in data_json:
                d = {}
                properties = record['Properties']
                d['game_date'] = game_date
                d['dfs_source'] = 'dk'
                d['dfs_contest_id'] = draft_group_id
                d['fantasy_result_id'] = properties['FantasyResultId']
                d['player_id'] = properties['PlayerId']
                d['player_name'] = properties['Player_Name']
                d['position'] = properties['Position']
                d['team'] = properties['Team']
                d['salary'] = properties['Salary']
                d['actual_points'] = properties['ActualPoints']
                d['ownership_average'] = properties['Average']
                d['ownership_volatility'] = properties['Volatility']
                d['gpp_grade'] = properties['GppGrade']
                d['fantasylabs_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
                d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                data.append(d)

        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        
        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_fantasylabs_ownership'
        replication_data['data'] = data
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        logger.log_text("FantasyLabs Ownership successfully scraped")
        return f'FantasyLabs Ownership successfully scraped'

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
