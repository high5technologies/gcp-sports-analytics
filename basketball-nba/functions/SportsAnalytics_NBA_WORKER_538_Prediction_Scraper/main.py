import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
import csv
import urllib.request

def nba_538_prediction_worker(event, context):

    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    try:

        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        startDate = datetime.strptime(message_data['startDate'], '%Y-%m-%d').date()
        endDate = datetime.strptime(message_data['endDate'], '%Y-%m-%d').date()
        historic_url = message_data['historic_url']

        if historic_url:
            url = "https://projects.fivethirtyeight.com/nba-model/nba_elo.csv"
        else:
            url = "https://projects.fivethirtyeight.com/nba-model/nba_elo_latest.csv"
                
        fivethirtyeight_data = []
        
        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',', quotechar='"')
            my_list = list(cr)
            i=1
            for row in my_list:
                if i>1:
                    r = {}
                    r['date'] = get_text(row[0])
                    r['season'] = get_text(row[1])
                    r['neutral'] = get_text(row[2])
                    r['playoff'] = get_text(row[3])
                    r['team1'] = get_text(row[4])
                    r['team2'] = get_text(row[5])
                    r['elo1_pre'] = get_text(row[6])
                    r['elo2_pre'] = get_text(row[7])
                    r['elo_prob1'] = get_text(row[8])
                    r['elo_prob2'] = get_text(row[9])
                    r['elo1_post'] = get_text(row[10])
                    r['elo2_post'] = get_text(row[11])
                    r['carm_elo1_pre'] = get_text(row[12])
                    r['carm_elo2_pre'] = get_text(row[13])
                    r['carm_elo_prob1'] = get_text(row[14])
                    r['carm_elo_prob2'] = get_text(row[15])
                    r['carm_elo1_post'] = get_text(row[16])
                    r['carm_elo2_post'] = get_text(row[17])
                    r['raptor1_pre'] = get_text(row[18])
                    r['raptor2_pre'] = get_text(row[19])
                    r['raptor_prob1'] = get_text(row[20])
                    r['raptor_prob2'] = get_text(row[21])
                    r['score1'] = get_text(row[22])
                    r['score2'] = get_text(row[23])
                    r['fivethirtyeight_key'] = r['date'] + '|' + r['team1'] + '|' + r['team2']
                    r['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                    # Only append data between start and end
                    game_date = datetime.strptime(r['date'], '%Y-%m-%d').date()
                    if game_date >= startDate and game_date <= endDate:
                        #print(game_date)
                        fivethirtyeight_data.append(r)
                    #print(row)
                i+=1
        
        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        

        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_538_predictions'
        replication_data['data'] = fivethirtyeight_data
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))

        return f'538 Predictions from GitHub successfully scraped'

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

def get_text(stat):
    if stat is not None:
        txt = stat.strip()
        if txt == "":
            txt = None
    else:
        txt = None
    return txt