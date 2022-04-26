import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import csv

def nba_538_scraper(request):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "nba_538_predictions_range_to_scrape"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)

    ##########################################################################
    # Inputs
    ##########################################################################

    # Test current or historic
    request_json = request.get_json()
    if request_json and 'Historic' in request_json:
        historic_url = True
    else:
        historic_url = False


    try:
        if request_json and 'StartDate' not in request_json:  
            startDate = datetime.strptime("1900-01-01", '%Y-%m-%d').date()
            
        else:
            startDate = datetime.strptime(request_json["StartDate"], '%Y-%m-%d').date()
        if request_json and 'EndDate' not in request_json:  
            endDate = datetime.strptime("9999-12-31", '%Y-%m-%d').date() 
        else:
            endDate = datetime.strptime(request_json["EndDate"], '%Y-%m-%d').date()
    except:
        raise ValueError("Start & End dates must be in YYYY-MM-DD format")
    


    ##########################################################################
    # Scrape FiveThirtyEight CSV
    ##########################################################################

    try:

        d = {}
        d['startDate'] = startDate
        d['endDate'] = endDate
        d['historic_url'] = historic_url

        data_string = json.dumps(d)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))   
        
        return f'538 Player Raptor season successfully queued'

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
            
    
