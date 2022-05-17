import base64
import json
from google.cloud import firestore
from datetime import datetime, timedelta, date
from google.cloud import logging

def common_error_log(event, context):
    try:

        # Get Mesage
        db = firestore.Client()
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        error_data = json.loads(pubsub_message)

        error_key = str(error_data['error_key'])
        function = str(error_data['function'])
        error_date_string = datetime.strptime(error_data['error_datetime'], '%Y-%m-%d %H:%M:%S').date().strftime('%Y-%m-%d')
        doc_ref = db.collection(u'error_log').document(error_date_string).collection(function).document(error_key)
        doc_ref.set(error_data)

    except Exception as e:
        #print(str(e))
        # Instantiate logging
        logging_client = logging.Client()
        log_name = os.environ.get('FUNCTION_NAME')
        logger = logging_client.logger(log_name)
        logger.log_text(str(e))
