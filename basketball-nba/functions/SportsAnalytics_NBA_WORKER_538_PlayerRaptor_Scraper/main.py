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

def nba_538_player_raptor_worker(event, context):

    # Config
    project_id = os.environ.get('GCP_PROJECT')
    topic_id = "bigquery_replication_topic"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    try:

        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        beginSeason = message_data['beginSeason']
        endSeason = message_data['endSeason']
        historic_url = message_data['historic_url']
        
        if historic_url:
            #url = "https://github.com/fivethirtyeight/data/blob/master/nba-raptor/modern_RAPTOR_by_team.csv"
            url = "https://raw.githubusercontent.com/fivethirtyeight/data/master/nba-raptor/modern_RAPTOR_by_team.csv"
        else:
            url = "https://projects.fivethirtyeight.com/nba-model/" + endSeason + "/latest_RAPTOR_by_team.csv"
                
        fivethirtyeight_data = []
        print(url)
        with requests.Session() as s:
            download = s.get(url)

            decoded_content = download.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',', quotechar='"')
            my_list = list(cr)
            i=1
            for row in my_list:
                if i>1:
                    r = {}
                    																						
                    r['player_name'] = get_text(row[0])
                    r['player_id'] = get_text(row[1])
                    r['season'] = get_text(row[2])
                    r['season_type'] = get_text(row[3])
                    r['team'] = get_text(row[4])
                    r['poss'] = get_text(row[5])
                    r['mp'] = get_text(row[6])
                    r['raptor_box_offense'] = get_text(row[7])
                    r['raptor_box_defense'] = get_text(row[8])
                    r['raptor_box_total'] = get_text(row[9])
                    r['raptor_onoff_offense'] = get_text(row[10])
                    r['raptor_onoff_defense'] = get_text(row[11])
                    r['raptor_onoff_total'] = get_text(row[12])
                    r['raptor_offense'] = get_text(row[13])
                    r['raptor_defense'] = get_text(row[14])
                    r['raptor_total'] = get_text(row[15])
                    r['war_total'] = get_text(row[16])
                    r['war_reg_season'] = get_text(row[17])
                    r['war_playoffs'] = get_text(row[18])
                    r['predator_offense'] = get_text(row[19])
                    r['predator_defense'] = get_text(row[20])
                    r['predator_total'] = get_text(row[21])
                    r['pace_impact'] = get_text(row[22])
                    r['fivethirtyeight_key'] = r['player_id'] + '|' + r['season'] + '|' + r['season_type'] + '|' + r['team']
                    r['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

                    # Only append data between start and end
                    season = int(r['season'])
                    if season >= int(beginSeason) and season <= int(endSeason):
                        #print(game_date)
                        fivethirtyeight_data.append(r)
                    #print(row)
                i+=1
        
        ##########################################################################
        # Publish to BigQuery Replication Topic
        ##########################################################################
        
        #print(fivethirtyeight_data)
        replication_data = {}
        replication_data['bq_dataset'] = 'nba' 
        replication_data['bq_table'] = 'raw_538_player_raptor'
        replication_data['data'] = fivethirtyeight_data
        data_string = json.dumps(replication_data)  
        future = publisher.publish(topic_path, data_string.encode("utf-8"))
        
        return f'538 Player Raptor data from GitHub successfully scraped'

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