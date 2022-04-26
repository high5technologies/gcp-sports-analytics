import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
from bs4 import BeautifulSoup, Comment

def nba_nbacom_scraper(request):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "nba_nbacom_dates_to_scrape"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    ##########################################################################
    # Input Data Check
    ##########################################################################

    try:
        request_json = request.get_json()
        if request_json and 'StartDate' not in request_json:  
            startDate = datetime.now().strftime("%Y-%m-%d")
        else:
            startDate = datetime.strptime(request_json['StartDate'], '%Y-%m-%d').date()
        if request_json and 'EndDate' not in request_json:  
            endDate = datetime.now().strftime("%Y-%m-%d") 
        else:
            endDate = datetime.strptime(request_json['EndDate'], '%Y-%m-%d').date()
    except:
        raise ValueError("Start & End dates must be in YYYY-MM-DD format")
    
    # Distinct list of Months between start and end date
    delta = endDate - startDate       # as timedelta
    
    if delta.days < 0:
        raise ValueError("StartDate can't be offer Begin Date")
    
    
    ##########################################################################
    # Get games/urls to scrape
    ##########################################################################
    
    try:
        for i in range(delta.days + 1):
            d = {}
            day = startDate + timedelta(days=i)
            d['date_string'] = day.strftime("%Y%m%d")
            d['date_formatted'] = day.strftime("%Y-%m-%d")
            
            data_string = json.dumps(d)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))        
                        
        return f'NBA.com dates queued successfully'

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
