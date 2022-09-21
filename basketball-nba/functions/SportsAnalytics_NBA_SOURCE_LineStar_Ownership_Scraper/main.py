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

def nba_linestar_ownership_schedule_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "nba_fantasylabs_ownership_schedule_scrape"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)
    
    ##########################################################################
    # Input Data Check
    ##########################################################################

    try:
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
        #game_date = message_data['date_string']

        if 'hist' in message_data:
            hist = True
        else:
            hist = False


        logger.log_text("hist:"+str(hist))

   
        ##########################################################################
        # Get games/urls to scrape
        ##########################################################################
        
        d = {}
        d['hist'] = hist
            
        data_string = json.dumps(d)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))        

        logger.log_text("LineStar Ownership dates queued successfully")     
        return f'LineStar Ownership dates queued successfully'

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

