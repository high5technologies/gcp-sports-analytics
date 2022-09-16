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

def nba_linestar_worker_schedule_scraper(event, context):

    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "nba_linestar_ownership_pids_to_scrape"
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
        hist = message_data['hist']

        # Get Current PID
        url = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetPeriodInformation?getLineupCnt=true&periodId=1&site=2&sport=2'
        logger.log_text("url:"+url)

        r = requests.get(url)
        #print(r.content[0:3000])
        json_string = r.content

        data = json.loads(json_string)

        max_pid = data['Info']['Periods'][0]['Id']

        # Get Max PID scraped from Firestore
        #docs = fs.collection(u'nba_scraper').document(u'linestar').collection('ownership').order_by(u'pid', direction=firestore.Query.DESCENDING).limit(1).stream()
        docs = fs.collection(u'nba_scraper').document(u'linestar').collection('ownership').stream()
    
        #cached_pid = 0 # default for first run (no cache)
        previously_ran_pids = []
        for doc in docs:
            d = doc.to_dict()
            #cached_pid = int(d['pid'])     
            previously_ran_pids.append(int(d['pid']))       

        # In hist mode, try running any pids that haven't been run
        if hist:
            for i in range(1,int(max_pid)+1):
                if i not in previously_ran_pids:
                    d = {}
                    d['pid'] = i
                    data_string = json.dumps(d)  
                    future = publisher.publish(topic_path, data_string.encode("utf-8")) 

        #if hist and cached_pid < max_pid:
        #    for pid in range(cached_pid+1, max_pid+1):
        #        d = {}
        #        d['pid'] = pid
        #        data_string = json.dumps(d)  
        #        future = publisher.publish(topic_path, data_string.encode("utf-8")) 

        if not hist:
            pid = max_pid
            d = {}
            d['pid'] = pid
            data_string = json.dumps(d)  
            future = publisher.publish(topic_path, data_string.encode("utf-8")) 

        ##########################################################################
        # Publish PIDs to scrape
        ##########################################################################

        logger.log_text("LineStar Schedule successfully queued PIDs")
        return f'LineStar Schedule successfully queued PIDs'

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
