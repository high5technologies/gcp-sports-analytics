import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
#from bs4 import BeautifulSoup, Comment
import urllib.request

def ahl_ahlcom_worker_individual_game_scraper(event, context):
    
    # Config
    #project_id = os.environ.get('GCP_PROJECT')
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    publisher = pubsub_v1.PublisherClient()
    topic_id = "bigquery_replication_topic"
    topic_path = publisher.topic_path(project_id, topic_id)
    fs = firestore.Client()

    try:
        
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        if 'game_id' in message_data and message_data['game_id'] != "" and message_data['game_id'] is not None:  
        
            g = {}
            g['game_date'] = message_data['game_date']
            g['game_id'] = message_data['game_id']
            g['game_status'] = message_data['game_status']
            g['home_team_city'] = message_data['home_team_city']
            g['visiting_team_city'] = message_data['visiting_team_city']
            g['home_goal_count'] = message_data['home_goal_count'] 
            g['visiting_goal_count'] = message_data['visiting_goal_count'] 
            g['schedule_key'] = message_data['schedule_key'] 
            g['load_datetime'] = message_data['load_datetime'] 
            g["season"] = message_data['season']  
            g["season_index"] = message_data['season_index'] 
            g["season_type"] = message_data['season_type'] 

            ##########################################################
            # box score
            
            # Raw Game JSON
            url_box = "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&view=gameSummary&game_id=" + str(g["game_id"]) + "&key=50c2cd9b5e18e390&client_code=ahl"
            response_box = requests.get(url_box)
            raw_json_box = json.loads(response_box.text[1:-1])
            #json_to_store_box = {"game_key" : game["game_id"], "game_date":game["game_date"], "load_datetime":load_datetime, "data":raw_json_box}
            #print(json_to_store_box)

            # Parse Data
            data_game = parse_box_game_data(g['game_id'], g['game_date'], g["season"], g["season_index"], g["season_type"], raw_json_box)
            data_goalie_log = parse_box_goalie_log(g['game_id'], g['game_date'], raw_json_box)
            data_goalie_box = parse_box_goalie_box(g['game_id'], g['game_date'], raw_json_box)
            data_skater_box = parse_box_skater_box(g['game_id'], g['game_date'], raw_json_box)
            data_refs = parse_box_ref(g['game_id'], g['game_date'], raw_json_box)
            data_coaches = parse_box_coaches(g['game_id'], g['game_date'], raw_json_box)
            data_game_mvp = parse_box_mvp(g['game_id'], g['game_date'], raw_json_box)
            

            # Load box score to pubsub
            #data_string = json.dumps(json_to_store_box)
            #future = publisher.publish(topic_path, data_string.encode("utf-8"))  
            # Game
            data_game_seq = []
            data_game_seq.append(data_game)
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl'
            replication_data['bq_table'] = 'raw_hockeytech_game'
            replication_data['data'] = data_game_seq
            data_string = json.dumps(replication_data)            
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # Goalie Log
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_goalielog'
            replication_data['data'] = data_goalie_log
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # Goalie Box
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_goaliebox'
            replication_data['data'] = data_goalie_box
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # Skater Box
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_skaterbox'
            replication_data['data'] = data_skater_box
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # Refs
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_ref'
            replication_data['data'] = data_refs
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # Coaches
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_coach'
            replication_data['data'] = data_coaches
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            # MVP
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_mvp'
            replication_data['data'] = data_game_mvp
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))


            ##########################################################
            # game log
            # Raw Game JSON
            url_game_log = "https://lscluster.hockeytech.com/feed/index.php?feed=statviewfeed&key=50c2cd9b5e18e390&client_code=ahl&view=gameCenterPlayByPlay&game_id=" + str(g["game_id"])
            response_game_log = requests.get(url_game_log)
            raw_json_game_log = json.loads(response_game_log.text[1:-1])
            #json_to_store_game_log = {"game_key" : game["game_id"], "game_date":game["game_date"], "load_datetime":load_datetime, "data":raw_json_game_log}
            #table_game_log.put_item(Item=json_to_store_game_log)
            #print(json_to_store_game_log)

            # Parse return JSON
            parsed_game_log = parse_game_log(g['game_id'], g['game_date'], raw_json_game_log)
            
            # BigQuery Replication
            replication_data = {}
            replication_data['bq_dataset'] = 'ahl' 
            replication_data['bq_table'] = 'raw_hockeytech_gamelog'
            replication_data['data'] = parsed_game_log
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))

            
            # Load box score to pubsub
            #data_string = json.dumps(json_to_store_game_log)
            #future = publisher.publish(topic_path, data_string.encode("utf-8")) 



            ##########################################################################
            # Store Schedule
            ##########################################################################   
                
            # Load schedule last (so no next execution only ignores games if successfully parsed)
            # Can't control the error if fails in replication ... should be smaller risk
            #for g in schedule:
                #print(g)
                #table_schedule.put_item(Item=g)
                #col_ref_key = str(dt) 
            #game_date = str(g['game_date'])
            #game_id = str(g['game_id'])
            fs.collection(u'AHL').document(u'schedule').collection(g['game_date']).document(g['game_id']).set(g)

        #if error_count == 0: 
        #    return 'Game Log successfully scraped'        
        #else:
        #    return 'Game log finished but errors occured.  See error log.'
        return 'Game Log successfully scraped'
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

def parse_box_game_data(game_key,game_date,season,season_index,season_type,data):
    
    ###########################################################################
    # Game data
    data_game = {}
    data_game['game_key'] = game_key
    data_game['game_date'] = game_date
    data_game['season'] = season
    data_game['season_index'] = season_index
    data_game['season_type'] = season_type
    data_game['attendance'] = data["details"]['attendance']
    data_game['duration'] = data["details"]['duration']
    data_game['start_time'] = data["details"]['startTime']
    data_game['end_time'] = data["details"]['endTime']
    data_game['started'] = data["details"]['started']
    data_game['final'] = data["details"]['final']
    data_game['status'] = data["details"]['status']
    data_game['venue'] = data["details"]['venue']
    data_game['has_shootout'] = data["hasShootout"]

    data_game['home_team_id'] = data["homeTeam"]["info"]["id"]
    data_game['home_team_abbrev'] = data["homeTeam"]["info"]["abbreviation"]
    data_game['home_team'] = data["homeTeam"]["info"]["name"]
    data_game['home_team_city'] = data["homeTeam"]["info"]["city"]
    data_game['home_team_name'] = data["homeTeam"]["info"]["nickname"]
    data_game['away_team_id'] = data["visitingTeam"]["info"]["id"]
    data_game['away_team_abbrev'] = data["visitingTeam"]["info"]["abbreviation"]
    data_game['away_team'] = data["visitingTeam"]["info"]["name"]
    data_game['away_team_city'] = data["visitingTeam"]["info"]["city"]
    data_game['away_team_name'] = data["visitingTeam"]["info"]["nickname"]
    
    data_game['home_assists'] = data["homeTeam"]["stats"]["assistCount"]
    data_game['home_goals'] = data["homeTeam"]["stats"]["goals"]
    data_game['home_hits'] = data["homeTeam"]["stats"]["hits"]
    data_game['home_infractions'] = data["homeTeam"]["stats"]["infractionCount"]
    data_game['home_pim'] = data["homeTeam"]["stats"]["penaltyMinuteCount"]
    data_game['home_ppgoals'] = data["homeTeam"]["stats"]["powerPlayGoals"]
    data_game['home_ppopps'] = data["homeTeam"]["stats"]["powerPlayOpportunities"]
    data_game['home_shots'] = data["homeTeam"]["stats"]["shots"]
    
    data_game['away_assists'] = data["visitingTeam"]["stats"]["assistCount"]
    data_game['away_goals'] = data["visitingTeam"]["stats"]["goals"]
    data_game['away_hits'] = data["visitingTeam"]["stats"]["hits"]
    data_game['away_infractions'] = data["visitingTeam"]["stats"]["infractionCount"]
    data_game['away_pim'] = data["visitingTeam"]["stats"]["penaltyMinuteCount"]
    data_game['away_ppgoals'] = data["visitingTeam"]["stats"]["powerPlayGoals"]
    data_game['away_ppopps'] = data["visitingTeam"]["stats"]["powerPlayOpportunities"]
    data_game['away_shots'] = data["visitingTeam"]["stats"]["shots"]
    
    data_game['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 

    return data_game

def parse_box_goalie_log(game_key,game_date,data):
    ###########################################################################
    # Goalie Log
    data_goalie_log = []
    for l in data["homeTeam"]["goalieLog"]:
        log = {}
        log["game_key"] = game_key
        log['game_date'] = game_date
        log["h_a"] = "H"
        log["goalie_id"] = l["info"]["id"]
        log["start_period"] = l["periodStart"]["shortName"]
        log["start_time"] = l["timeStart"]
        log["end_period"] = l["periodEnd"]["shortName"]
        log["end_time"] = l["timeEnd"]
        log['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        log['goalie_log_key'] = game_key + '|' + str(log["goalie_id"]) + '|' + str(log["start_period"])  + '|' + str(log["start_time"])
        data_goalie_log.append(log)
    for l in data["visitingTeam"]["goalieLog"]:
        log = {}
        log["game_key"] = game_key
        log['game_date'] = game_date
        log["h_a"] = "H"
        log["goalie_id"] = l["info"]["id"]
        log["start_period"] = l["periodStart"]["shortName"]
        log["start_time"] = l["timeStart"]
        log["end_period"] = l["periodEnd"]["shortName"]
        log["end_time"] = l["timeEnd"]
        log['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        log['goalie_log_key'] = game_key + '|' + str(log["goalie_id"]) + '|' + str(log["start_period"])  + '|' + str(log["start_time"])
        data_goalie_log.append(log)

    return data_goalie_log

def parse_box_goalie_box(game_key,game_date,data):
    ###########################################################################
    # Goalie box
    data_goalie_box = []
    for g in data["homeTeam"]["goalies"]:
        b = {}
        b["game_key"] = game_key 
        b['game_date'] = game_date
        b["h_a"] = "H"
        b["birth_date"] = g["info"]["birthDate"]
        b["first_name"] = g["info"]["firstName"]
        b["last_name"] = g["info"]["lastName"]
        b["goalie_id"] = g["info"]["id"]
        b["jersey_number"] = g["info"]["jerseyNumber"]
        b["position"] = g["info"]["position"]
        b["starting"] = g["starting"]
        b["assists"] = g["stats"]["assists"]
        b["goals"] = g["stats"]["goals"]
        b["goals_against"] = g["stats"]["goalsAgainst"]
        b["pim"] = g["stats"]["penaltyMinutes"]
        b["plus_minus"] = g["stats"]["plusMinus"]
        b["points"] = g["stats"]["points"]
        b["saves"] = g["stats"]["saves"]
        b["shots_against"] = g["stats"]["shotsAgainst"]
        b["time_on_ice"] = g["stats"]["timeOnIce"]
        b["status"] = g["status"]
        b['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        b['goalie_box_key'] = game_key + '|' + str(b["goalie_id"])
        data_goalie_box.append(b)
        
    for g in data["visitingTeam"]["goalies"]:
        b = {}
        b["game_key"] = game_key 
        b['game_date'] = game_date
        b["h_a"] = "A"
        b["birth_date"] = g["info"]["birthDate"]
        b["first_name"] = g["info"]["firstName"]
        b["last_name"] = g["info"]["lastName"]
        b["goalie_id"] = g["info"]["id"]
        b["jersey_number"] = g["info"]["jerseyNumber"]
        b["position"] = g["info"]["position"]
        b["starting"] = g["starting"]
        b["assists"] = g["stats"]["assists"]
        b["goals"] = g["stats"]["goals"]
        b["goals_against"] = g["stats"]["goalsAgainst"]
        b["pim"] = g["stats"]["penaltyMinutes"]
        b["plus_minus"] = g["stats"]["plusMinus"]
        b["points"] = g["stats"]["points"]
        b["saves"] = g["stats"]["saves"]
        b["shots_against"] = g["stats"]["shotsAgainst"]
        b["time_on_ice"] = g["stats"]["timeOnIce"]
        b["status"] = g["status"]    
        b['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        b['goalie_box_key'] = game_key + '|' + str(b["goalie_id"])
        data_goalie_box.append(b)

    return data_goalie_box

def parse_box_skater_box(game_key,game_date,data):
    ###########################################################################
    # Skater box
    data_skater_box = []
    for g in data["homeTeam"]["skaters"]:
        b = {}
        b["game_key"] = game_key 
        b['game_date'] = game_date
        b["h_a"] = "H"
        b["birth_date"] = g["info"]["birthDate"]
        b["first_name"] = g["info"]["firstName"]
        b["last_name"] = g["info"]["lastName"]
        b["skater_id"] = g["info"]["id"]
        b["jersey_number"] = g["info"]["jerseyNumber"]
        b["position"] = g["info"]["position"]
        b["starting"] = g["starting"]
        b["assists"] = g["stats"]["assists"]
        b["goals"] = g["stats"]["goals"]
        b["hits"] = g["stats"]["hits"]
        b["pim"] = g["stats"]["penaltyMinutes"]
        b["plus_minus"] = g["stats"]["plusMinus"]
        b["points"] = g["stats"]["points"]
        b["shots"] = g["stats"]["shots"]
        b["status"] = g["status"]
        b['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        b['skater_box_key'] = b["game_key"] + '|' + str(b["skater_id"])
        data_skater_box.append(b)
    for g in data["visitingTeam"]["skaters"]:
        b = {}
        b["game_key"] = game_key 
        b['game_date'] = game_date
        b["h_a"] = "A"
        b["birth_date"] = g["info"]["birthDate"]
        b["first_name"] = g["info"]["firstName"]
        b["last_name"] = g["info"]["lastName"]
        b["skater_id"] = g["info"]["id"]
        b["jersey_number"] = g["info"]["jerseyNumber"]
        b["position"] = g["info"]["position"]
        b["starting"] = g["starting"]
        b["assists"] = g["stats"]["assists"]
        b["goals"] = g["stats"]["goals"]
        b["hits"] = g["stats"]["hits"]
        b["pim"] = g["stats"]["penaltyMinutes"]
        b["plus_minus"] = g["stats"]["plusMinus"]
        b["points"] = g["stats"]["points"]
        b["shots"] = g["stats"]["shots"]
        b["status"] = g["status"]
        b['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        b['skater_box_key'] = b["game_key"] + '|' + str(b["skater_id"])
        data_skater_box.append(b)

    return data_skater_box

def parse_box_ref(game_key,game_date,data):
    ###########################################################################
    # Refs/Linesmen
    data_refs = []

    # Ref/Linesman data
    for l in data["linesmen"]:
        ref = {}
        ref['game_key'] = game_key
        ref['game_date'] = game_date
        ref['first_name'] = l['firstName']
        ref['last_name'] = l['lastName'] 
        ref['role'] = l['role']
        ref['jersey_number'] = l['jerseyNumber']
        ref['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        ref['game_ref_key'] = game_key + '|' + str(ref['jersey_number'])
        data_refs.append(ref)
    
    for r in data["referees"]:
        ref = {}
        ref['game_key'] = game_key
        ref['game_date'] = game_date
        ref['first_name'] = r['firstName']   
        ref['last_name'] = r['lastName'] 
        ref['role'] = r['role']
        ref['jersey_number'] = r['jerseyNumber']
        ref['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        ref['game_ref_key'] = game_key + '|' + str(ref['jersey_number'])
        data_refs.append(ref)

    return data_refs   

def parse_box_coaches(game_key,game_date,data):
    ###########################################################################
    # Coaches
    data_coaches = []
    for c in data["homeTeam"]["coaches"]:
        coach = {}
        coach["game_key"] = game_key
        coach['game_date'] = game_date
        coach["team"] = data["homeTeam"]["info"]["abbreviation"]
        coach["h_a"] = "H"
        coach["first_name"] = c["firstName"]
        coach["last_name"] = c["lastName"]
        coach["role"] = c["role"]
        coach['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        coach['game_coach_key'] = game_key + '|' + str(coach["team"]) + '|' + str(coach["first_name"]) + ' ' + str(coach["last_name"])
        data_coaches.append(coach)
    for c in data["visitingTeam"]["coaches"]:
        coach = {}
        coach["game_key"] = game_key
        coach['game_date'] = game_date
        coach["team"] = data["visitingTeam"]["info"]["abbreviation"]
        coach["h_a"] = "A"
        coach["first_name"] = c["firstName"]
        coach["last_name"] = c["lastName"]
        coach["role"] = c["role"]
        coach['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        coach['game_coach_key'] = game_key + '|' + str(coach["team"]) + '|' + str(coach["first_name"]) + ' ' + str(coach["last_name"])
        data_coaches.append(coach)
            
    return data_coaches

def parse_box_mvp(game_key,game_date,data):
    ###########################################################################
    # Game MVP
    data_game_mvp = []
    for mvp in data["mostValuablePlayers"]:
        m = {}
        m["game_key"] = game_key
        m['game_date'] = game_date
        m["player_id"] = mvp["player"]["info"]["id"]
        m["position"] = mvp["player"]["info"]["position"]
        m["starting"] = mvp["player"]["starting"]
        m["team_id"] = mvp["team"]["id"]
        m["team_abbrev"] = mvp["team"]["abbreviation"]
        m['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        m['game_mvp_key'] = game_key + '|' + str(m["player_id"])
        data_game_mvp.append(m)

    return data_game_mvp

def parse_game_log(game_key,game_date,data):
    #data = message_data['data']
    #game_key = message_data['game_key']
    #game_date = message_data['game_date']
    #print(str(game_date) + '|' + str(game_key))
    
    game_log = []
    log_cnt = 1
    for l in data:
        item = {}
        event = l["event"]
        details = l["details"]
        details_keys = list(details.keys())
        
        item['game_key'] = game_key 
        item['game_date'] = game_date
        item['event_type'] = event
        if event == 'shootout':
            item['period'] = 'SO'
            item['time'] = ""
        else:
            item['period'] = details['period']['shortName']
            item['time'] = details['time']
        
        
        # team_id (different by event_type)
        if event == 'penalty':
            item['team_id'] = details['againstTeam']['id']
        elif event == 'shot':
            item['team_id'] = details['shooterTeamId'] if ("shooterTeamId" in details_keys and details['shooterTeamId'] is not None) else ""
        elif event == 'goal':
            item['team_id'] = details['team']['id'] if ("team" in details_keys and details['team']['id'] is not None) else ""
        elif event == 'shootout':
            item['team_id'] = details['shooterTeam']['id']
        elif event == 'penaltyshot':
            item['team_id'] = details['shooter_team']['id']
        else:
            item['team_id'] = details['team_id'] if ("team_id" in details_keys and details['team_id'] is not None) else ""
        
        # player_id
        if event == 'penalty':
            item['player_id'] = details['takenBy']['id']
        else:
            item['player_id'] = details['shooter']['id'] if ("shooter" in details_keys and details['shooter']['id'] is not None) else ""
        
        
        
        # Shot
        item['shot_is_goal'] = details['isGoal'] if ("isGoal" in details_keys and details['isGoal'] is not None) else None
        #item['shooter_team_id'] = details['shooterTeamId'] if ("shooterTeamId" in details_keys and details['shooterTeamId'] is not None) else ""
        item['shot_type'] = details['shotType'] if ("shotType" in details_keys and details['shotType'] is not None) else ""
        item['shot_quality'] = details['shotQuality'] if ("shotQuality" in details_keys and details['shotQuality'] is not None) else ""
        item['x_location'] = details['xLocation'] if ("xLocation" in details_keys and details['xLocation'] is not None) else ""
        item['y_location'] = details['yLocation'] if ("yLocation" in details_keys and details['yLocation'] is not None) else ""
        item['goalie_id'] = details['goalie']['id'] if ("goalie" in details_keys and details['goalie']['id'] is not None) else ""
        #item['shooter_id'] = details['shooter']['id'] if ("shooter" in details_keys and details['shooter']['id'] is not None) else ""
        item['shooter_position'] = details['shooter']['position'] if ("shooter" in details_keys and details['shooter']['position'] is not None) else ""
        
        # Goal
        #item['goal_team_id'] = details['team']['id'] if ("team" in details_keys and details['team']['id'] is not None) else ""
        item['empty_net'] = details['properties']['isEmptyNet'] if ("team" in details_keys and details['properties']['isEmptyNet'] is not None) else ""
        
        # This part sucks - sometimes it's returned as 1/0, others true/false - convert to 1/0 for consistency in RAW layer
        if event == 'shootout':
            if "isGameWinningGoal" in details_keys and details['isGameWinningGoal'] is not None:
                if type(details['isGameWinningGoal']) == bool:
                    if details['isGameWinningGoal']:
                        item['game_winning_goal_flag'] = "1"
                    elif not details['isGameWinningGoal']:
                        item['game_winning_goal_flag'] = "0"
                else:
                    item['game_winning_goal_flag'] = details['isGameWinningGoal']
            else:
                item['game_winning_goal_flag'] = None
        else:
            if ("team" in details_keys and details['properties']['isGameWinningGoal'] is not None):
                if type(details['properties']['isGameWinningGoal']) == bool:
                    if details['properties']['isGameWinningGoal']:
                        item['game_winning_goal_flag'] = "1"
                    elif not details['properties']['isGameWinningGoal']:
                        item['game_winning_goal_flag'] = "0"
                else:
                    item['game_winning_goal_flag'] = details['properties']['isGameWinningGoal'] 
            else:
                item['game_winning_goal_flag'] = None
        item['insurance_goal_flag'] = details['properties']['isInsuranceGoal'] if ("team" in details_keys and details['properties']['isInsuranceGoal'] is not None) else ""
        item['penalty_shot_flag'] = details['properties']['isPenaltyShot'] if ("team" in details_keys and details['properties']['isPenaltyShot'] is not None) else ""
        item['power_play'] = details['properties']['isPowerPlay'] if ("team" in details_keys and details['properties']['isPowerPlay'] is not None) else ""
        item['short_handed'] = details['properties']['isShortHanded'] if ("team" in details_keys and details['properties']['isShortHanded'] is not None) else ""
        item["primary_assist_player_id"] = details['assists'][0]['id'] if ("assists" in details_keys and len(details['assists']) >= 1 and details['assists'][0]['id'] is not None) else ""
        item["secondary_assist_player_id"] = details['assists'][1]['id'] if ("assists" in details_keys and len(details['assists']) >= 2 and details['assists'][1]['id'] is not None) else ""
        
        item["minus_player_id_1"] = details['minus_players'][0]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 1 and details['minus_players'][0]['id'] is not None) else ""
        item["minus_player_id_2"] = details['minus_players'][1]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 2 and details['minus_players'][1]['id'] is not None) else ""
        item["minus_player_id_3"] = details['minus_players'][2]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 3 and details['minus_players'][2]['id'] is not None) else ""
        item["minus_player_id_4"] = details['minus_players'][3]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 4 and details['minus_players'][3]['id'] is not None) else ""
        item["minus_player_id_5"] = details['minus_players'][4]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 5 and details['minus_players'][4]['id'] is not None) else ""
        item["minus_player_id_6"] = details['minus_players'][5]['id'] if ("minus_players" in details_keys and len(details['minus_players']) >= 6 and details['minus_players'][5]['id'] is not None) else ""
        #details['minus_players'][3]
        
        item["plus_player_id_1"] = details['plus_players'][0]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 1 and details['plus_players'][0]['id'] is not None) else ""
        item["plus_player_id_2"] = details['plus_players'][1]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 2 and details['plus_players'][1]['id'] is not None) else ""
        item["plus_player_id_3"] = details['plus_players'][2]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 3 and details['plus_players'][2]['id'] is not None) else ""
        item["plus_player_id_4"] = details['plus_players'][3]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 4 and details['plus_players'][3]['id'] is not None) else ""
        item["plus_player_id_5"] = details['plus_players'][4]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 5 and details['plus_players'][4]['id'] is not None) else ""
        item["plus_player_id_6"] = details['plus_players'][5]['id'] if ("plus_players" in details_keys and len(details['plus_players']) >= 6 and details['plus_players'][5]['id'] is not None) else ""
        
        
        # Goalie in/out
        item['goalie_coming_in_id'] = details["goalieComingIn"]["id"] if ("goalieComingIn" in details_keys and details["goalieComingIn"] is not None and details["goalieComingIn"]["id"] is not None) else None
        item['goalie_coming_out_id'] = details["goalieGoingOut"]["id"] if ("goalieGoingOut" in details_keys and details["goalieGoingOut"] is not None and details["goalieGoingOut"]["id"] is not None) else None
        
        # Penalties
        item['penalty'] = details['description'] if ("description" in details_keys and details['description'] is not None) else ""
        item['pim'] = details['minutes'] if ("minutes" in details_keys and details['minutes'] is not None) else ""
        item['penalty_is_power_play'] = details['isPowerPlay'] if ("isPowerPlay" in details_keys and details['isPowerPlay'] is not None) else None
        item['penalty_servered_by_player_id'] = details['servedBy']['id'] if ("servedBy" in details_keys and details['servedBy']['id'] is not None) else ""
        
        # game_log_key
        item['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        item['game_log_key'] = item['game_key'] + '|' + str(log_cnt)
        
        game_log.append(item)
        log_cnt += 1

    return game_log
    