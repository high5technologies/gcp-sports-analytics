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
from google.cloud import firestore
from google.cloud import storage
from io import StringIO

def bigquery_datastore_reverseetl(event, context):
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
    fs = firestore.Client()

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
        
        bucket_name = 'reverse_etl_export'
        file_name = bq_dataset + '_' + bq_table + '_' + bq_filter + '_' + bq_filter_value + '.json'
        reverse_etl_table_name = 'retl_' + bq_dataset + '_' + bq_table + '_' + bq_filter + '_' + bq_filter_value.replace("-", "")
        #reverse_etl_table_name = reverse_etl_table_name.replace("-", "")

        # Create table to extract
        query = "CREATE OR REPLACE TABLE reverseetl." + reverse_etl_table_name + " as SELECT * FROM " + bq_dataset + "." + bq_table + " WHERE " + bq_filter + " = '" + bq_filter_value + "';"
        logger.log_text(query)
        #job_config = bigquery.QueryJobConfig(
        #    query_parameters=[
        #        bigquery.ScalarQueryParameter("corpus", "STRING", "romeoandjuliet"),
        #        bigquery.ScalarQueryParameter("min_word_count", "INT64", 250),
        #    ]
        #)
        #query_job = client.query(query, job_config=job_config)  # Make an API request.
        query_job = client.query(query)  # Make an API request.
        query_job.result()  # Waits for statement to finish

        
        destination_uri = "gs://{}/{}".format(bucket_name, file_name)
        dataset_ref = bigquery.DatasetReference(project_id, 'reverseetl')
        table_ref = dataset_ref.table(reverse_etl_table_name)
        job_config = bigquery.job.ExtractJobConfig()
        job_config.destination_format = bigquery.DestinationFormat.NEWLINE_DELIMITED_JSON
        #job_config.field_delimiter = 

        logger.log_text("gs:" + bucket_name + "/" + file_name)

        extract_job = client.extract_table(
            table_ref,
            destination_uri,
            job_config=job_config,
            # Location must match that of the source table.
            location="US",
        )  # API request
        extract_job.result()  # Waits for job to complete.

        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(file_name)
        content_string = blob.download_as_string().decode('utf-8')
        #content_string = StringIO(content_blob) 
        json_strings = content_string.split('\n')

        for json_string in json_strings:
            json_data = json.loads(json_string)
            unique_key = json_data['unique_key']
            fs.collection(u'sports_analytics').document(bq_dataset).collection(bq_table).document(unique_key).set(json_data)
        
        # Create table to extract
        query = "DROP TABLE reverseetl." + reverse_etl_table_name
        query_job = client.query(query)  # Make an API request.
        query_job.result()  # Waits for statement to finish

        return f'Data successfully replicated from BigQuery to Datastore'

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
        


     