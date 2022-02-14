import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
#from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
#from bs4 import BeautifulSoup, Comment
import urllib.request

def ahl_roster_team_scraper(event, context):
    
    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    topic_id = "bigquery_replication_topic"
    topic_path = publisher.topic_path(project_id, topic_id)
    #fs = firestore.Client()

    try:
            
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        season_index = message_data['season_index']
        team_id = message_data['team_id']
        
        url_roster = "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=roster&team_id=" + str(team_id)  + "&season_id=" + str(season_index) + "&key=50c2cd9b5e18e390&client_code=ahl&league_id=4&lang=en"
        response_roster = requests.get(url_roster) 
        #raw_json_roster = json.loads(response_roster.text[1:-1])
        data = raw_json_roster = json.loads(response_roster.text[1:-1])
        roster_key = str(season_index) + "|" + str(team_id)
        load_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #json_to_store_roster = {"roster_key" : roster_key, "season_index":str(season_index), "team_id":str(team_id), "load_datetime":load_datetime, "data":raw_json_roster}
        
        #roster_key = message_data['roster_key']
        #season =  message_data['season']
        #team_id = message_data['team_id']
        #load_datetime = message_data['load_datetime']
        #data = message_data['data']

        print(str(roster_key) + '...' + str(season_index) + '...' + str(team_id))

        
        if(team_id) != -1: 
            roster = []
            for section in data["roster"][0]["sections"]:
                title = section["title"]
                if title in ["Forwards","Defencemen","Goalies"]:
                    for player in section["data"]:
                        p = {}
                        p["season_index"] = season_index
                        p["team_id"] = team_id
                        if( title == "Goalies" ):
                            p["catches"] = player["row"]["catches"]
                            p["shoots"] = ""
                        else:
                            p["catches"] = ""
                            p["shoots"] = player["row"]["shoots"]
                            
                        p["birthplace"] = player["row"]["birthplace"]
                        p["height"] = player["row"]["height_hyphenated"]
                        p["player_id"] = player["row"]["player_id"]
                        p["birthdate"] = player["row"]["birthdate"]
                        p["jersey_number"] = player["row"]["tp_jersey_number"]
                        p["position"] = player["row"]["position"]
                        p["weight"] = player["row"]["w"]
                        p["name"] = player["row"]["name"]
                        p["roster_key"] = str(season_index) + "|" + str(team_id) + "|" + str(p["player_id"])
                        p["load_datetime"] = load_datetime
                        roster.append(p)
                        #print(p)

            #print(roster)

            # Publish to BigQuery replication topic
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl'
            replication_data['bq_table'] = 'raw_hockeytech_roster'
            replication_data['data'] = roster
            data_string = json.dumps(replication_data)            
            future = publisher.publish(topic_path, data_string.encode("utf-8"))


        #start here 2/9 @ sports sample ... finish this logic and add logic from map
        return f'ahl.com schedule successfully scraped'
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

        # Log error
        topic_id_error = "error_log_topic"
        data_string_error = json.dumps(err) 
        topic_path_error = publisher.topic_path(project_id, topic_id_error)
        future = publisher.publish(topic_path_error, data_string_error.encode("utf-8"))
        
       

        






