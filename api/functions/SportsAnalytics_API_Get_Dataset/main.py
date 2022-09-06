import json
import os
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
from google.cloud import logging
import uuid
import traceback
import urllib.request

def api_return_data(request):
    
    

    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    
    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)
    
    try:
        #request_json = request.get_json()
        #if not request_json: 
        #    raise ValueError("Invalid inputs - none supplied")
        #if 'league' not in request_json:  
        #    raise ValueError("invalid inputs - league is a required input")
        #if 'dataset' not in request_json:
        #    raise ValueError("invalid inputs - dataset is a required input")
        #if 'season' not in request_json:
        #    raise ValueError("invalid inputs - season is a required input")
        #
        #league = request_json["league"]
        #dataset = request_json["dataset"]
        #season = request_json["season"]

        request_args = request.args

        if not request_args: 
            raise ValueError("Invalid inputs - none supplied")
        if 'league' not in request_args:  
            raise ValueError("invalid inputs - league is a required input")
        if 'dataset' not in request_args:
            raise ValueError("invalid inputs - dataset is a required input")
        #if 'season' not in request_args:
        #    raise ValueError("invalid inputs - season is a required input")
        
        league = request_args["league"]
        dataset = request_args["dataset"]
        #season = request_args["season"]

    except:
        raise ValueError("invalid inputs")

    try:
        bq_table = 'api_' + dataset

        fs = firestore.Client()
        #docs = fs.collection(u'sports_analytics').document(league).collection(bq_table).where('season','==', season).stream()
        docs = fs.collection(u'sports_analytics').document(league).collection(bq_table).stream()
        #docs = fs.collection('users').where('paid', '==', True).stream()
        data = []
        for doc in docs:
            #print(doc.id)
            #print(doc.to_dict())
            data.append(doc.to_dict())

        headers = {
            'Access-Control-Allow-Origin': '*'
        }

        #return_data = {"data":data}
        #return {"data":data}    
        #return data
        return ({"data":data}, 200, headers)
        #return f'NBA.com dates queued successfully'

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
