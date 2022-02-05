import json
import os
from google.cloud import pubsub_v1
#import base64
#import uuid
#import traceback
#from bs4 import BeautifulSoup, Comment

def bigquery_load_test(request):
    
    # Config
    project_id = os.environ.get('GCP_PROJECT')
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    # Create test data
    data = []
    data.append({"key":1,"val":"a"})
    data.append({"key":2,"val":"b"})
    data.append({"key":3,"val":"c"})

    # Push test data to bigquery replication topic
    replication_data = {}
    replication_data['bq_dataset'] = 'common' 
    replication_data['bq_table'] = 'test_data'
    replication_data['data'] = data
    data_string = json.dumps(replication_data)  
    future = publisher.publish(topic_path, data_string.encode("utf-8"))   

    return f'Test data sent to bigquery replication'
