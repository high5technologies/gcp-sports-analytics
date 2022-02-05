import base64
import json
from google.cloud import bigquery
from google.cloud import pubsub_v1
import os
from datetime import datetime, timedelta, date
import uuid
import traceback

def pubsub_to_bigquery_replication(event, context):
    """Triggered from a message on a Cloud Pub/Sub topic.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    client = bigquery.Client()
    project_id = os.environ.get('GCP_PROJECT')
    
    publisher = pubsub_v1.PublisherClient()
    try:
        # decode message from pubsub
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
        #print(message_data)

        # BigQuery table
        bq_dataset = message_data['bq_dataset']
        bq_table = message_data['bq_table']
        table_id = project_id + "." + bq_dataset + "." + bq_table

        #data = json.loads(message_data['data'])
        data = message_data['data']
        errors = client.insert_rows_json(table_id, data)  # Make an API request.
        
        if errors == []:
            print("New rows have been added.")
        else:
            print("Encountered errors while inserting rows: {}".format(errors))
            raise ValueError(json.dumps(errors))
            
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
        


     