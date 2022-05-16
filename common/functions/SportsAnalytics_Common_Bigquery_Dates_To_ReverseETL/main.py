import base64
import json
from google.cloud import bigquery
from google.cloud import pubsub_v1
import os
from datetime import datetime, timedelta, date
import uuid
import traceback
#import pandas as pd
#import pandas_gbq
import urllib.request
from google.cloud import logging

def pubsub_to_bigquery_replication(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    client = bigquery.Client()
    #project_id = os.environ.get('GCP_PROJECT')
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()

    # Instantiate logging
    logging_client = logging.Client()
    log_name = os.environ.get('FUNCTION_NAME')
    logger = logging_client.logger(log_name)

    # bucket_name = 'my-bucket'
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    message_data = json.loads(pubsub_message)

    bq_tables_string = message_data['tables']
    bq_tables = bq_tables_string.split(',')

    try:
        if 'start_date' not in message_data:  
            start_date = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            start_date = datetime.strptime(message_data['start_date'], '%Y-%m-%d').date()
        if 'end_date' not in message_data:  
            end_date = (datetime.now() - timedelta(1)).date() #.strftime('%Y-%m-%d')
        else:
            end_date = datetime.strptime(message_data['end_date'], '%Y-%m-%d').date()
    except:
        raise ValueError("Start & End dates must be in YYYY-MM-DD format")

    logger.log_text("tables:" + bq_tables_string + "; start_date: " + start_date + "; end_date:" + end_date)

    # Distinct list of Months between start and end date
    delta = end_date - start_date       # as timedelta
    
    if delta.days < 0:
        raise ValueError("StartDate can't be offer Begin Date")
    
    try:
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            #d['date_string'] = day.strftime("%Y%m%d")
            #d['date_formatted'] = day.strftime("%Y-%m-%d")
            game_date = day.strftime("%Y-%m-%d")

            for schema_table in bq_tables:
                d = {}
                d['dataset'] = schema_table.split(".")[0]
                d['table'] = schema_table.split(".")[1]
                d['filter'] = 'game_date'
                d['filter_value'] = game_date

                data_string = json.dumps(d) 
                topic_id = "bigquery_datastore_reverseetl"
                topic_path = publisher.topic_path(project_id, topic_id)
                future = publisher.publish(topic_path, data_string.encode("utf-8"))    


        #bq_dataset = message_data['dataset']
        #bq_table = message_data['table']
        #bq_filter = message_data['filter']
        #bq_filter_value = message_data['filter_value']
         
        return f'Data successfully pushed to reverse etl topic'

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
        


     