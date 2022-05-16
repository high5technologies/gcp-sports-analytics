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

    try:
        
        # decode message from pubsub
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)
        
        bq_dataset = message_data['dataset']
        bq_table = message_data['table']
        bq_filter = message_data['filter']
        bq_filter_value = message_data['filter_value']
        
        bucket_name = bq_dataset + '_' + bq_table
        file_name = bq_table + '_' + bq_filter + '_' + bq_filter_value + '.json'

        destination_uri = "gs://{}/{}".format(bucket_name, file_name)
        dataset_ref = bigquery.DatasetReference(project_id, bq_dataset)
        table_ref = dataset_ref.table(bq_table)
        job_config = bigquery.job.ExtractJobConfig()
        job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON

        logger.log_text("gs:" + bucket_name + "/" + file_name)

        extract_job = client.extract_table(
            table_ref,
            destination_uri,
            job_config=job_config,
            # Location must match that of the source table.
            location="US",
        )  # API request
        extract_job.result()  # Waits for job to complete.

        #bucket = storage_client.get_bucket(bucket_name)
        #blob = bucket.blob(dfile_name)
        #contents = blob.download_as_string()

        #json_object = json.loads(contents)


        
        #DATA_FILE = os.path.join(os.path.dirname(__file__), 'YOUR_DATA_FILE.json')
        #with open(DATA_FILE, 'r') as dataFile:
        #    JSON_DATA = json.loads(dataFile.read())
         
        return f'Data successfully replicated to BigQuery'

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
        


     