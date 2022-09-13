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

def format_js_object(g):
    g = g.replace("'",'"')
    g = g.replace(" ","").replace('\r', '').replace('\n', '')
    g = g.replace('{','{"')
    g = g.replace('}','"}')
    g = g.replace(':','":"')
    g = g.replace(',','","')
    g = g.replace('""','"')
    g = g.replace(':"[',':[')
    g = g.replace(']","','],')
    g = g.replace('}","','},')
    g = g.replace('},]','}]')
    g = g.replace('],}',']}')
    g = g.replace('{"}','{}')
    return g

def extract_json_string_from_html(html, find_string):
    base_index = html.find(find_string)
    start = html.find("{",base_index)
    end = html.find(";",start)
    json_string = html[start:end]
    json_string = format_js_object(json_string)
    return json_string


def nba_linestar_worker_individual_ownership_scraper(event, context):

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

    fs = firestore.Client()

    try:

        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        #game_date = message_data['date_formatted']
        #game_url_id = message_data['url_id']
        #game_key = message_data['game_key']
        #date_string = message_data['date_string']
        #games = message_data['games']
        pid = message_data['pid']

        dfs_sources = ['FanDuel','DraftKings']
        for dfs_source in dfs_sources:
            #dfs_source = 'FanDuel'

            url = 'https://www.linestarapp.com/Ownership/Sport/NBA/Site/' + dfs_source + '/PID/' + str(pid)

            r = requests.get(url)
            #print(r.content[0:3000])
            page_content = r.content
            soup = BeautifulSoup(page_content, 'html.parser')
            scripts = soup.find_all("script")
            script_with_date_field = ""
            script_with_data = ""
            data = []

            #################################################
            # Extract Game Date (since all we get is the PID)
            is_found = False
            for script in scripts:
                if 'fscInfo' in str(script):
                    script_with_date_field = str(script)
                    is_found = True
                    break

            base_index = script_with_date_field.find('fscInfo')
            base_index_2 = script_with_date_field.find("periodName",base_index)
            start = script_with_date_field.find('"',base_index) + 1
            end = script_with_date_field.find('",',start)
            game_date_string = script_with_date_field[start:end]
            game_date_timestamp = datetime.strptime(game_date_string, '%b %d, %Y')
            game_date = game_date_timestamp.strftime('%Y-%m-%d')
            
            #################################################
            # Find Data
            is_found = False
            for script in scripts:
                if 'projectedSlatesDict' in str(script):
                    script_with_data = str(script)
                    is_found = True
                    break

            # Projected
            projected_json_string = extract_json_string_from_html(script_with_data,'projectedSlatesDict')
            projected_json = json.loads(projected_json_string)

            for key in projected_json.keys():
                arr = projected_json[key]
                for record in arr:
                    d = {}
                    d['game_date'] = game_date
                    d['pid'] = pid
                    d['dfs_source'] = dfs_source
                    d['dfs_contest_id'] = key
                    d['linestar_type'] = 'projected'
                    d['player_id'] = record['id']
                    d['player_name'] = record['name']
                    d['owned'] = record['owned']
                    d['player_pos'] = record['pos']
                    d['team'] = record['team']
                    d['player_salary'] = record['sal']
                    d['linestar_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
                    d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    data.append(d)


            # Actual
            actual_json_string = extract_json_string_from_html(script_with_data,'actualResultsDict')
            actual_json = json.loads(actual_json_string)

            for key in actual_json.keys():
                arr = actual_json[key]
                for record in arr:
                    d = {}
                    d['game_date'] = game_date
                    d['pid'] = pid
                    d['dfs_source'] = dfs_source
                    d['dfs_contest_id'] = key
                    d['linestar_type'] = 'actual'
                    d['player_id'] = record['id']
                    d['player_name'] = record['name']
                    d['owned'] = record['owned']
                    d['player_pos'] = record['pos']
                    d['team'] = record['team']
                    d['player_salary'] = record['sal']
                    d['linestar_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
                    d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                    data.append(d)

                    
        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        
        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_linestar_ownership'
        replication_data['data'] = data
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        # Update Firestore to store that PID was updated
        pid_data = {}
        pid_data['pid'] = pid
        doc_ref = fs.collection(u'nba_scraper').document(u'linestar').collection('ownership').document(pid)
        doc_ref.set(pid_data)

        logger.log_text("LineStar Ownership successfully scraped")
        return f'LineStar Ownership successfully scraped'

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
