import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from google.cloud import firestore
from google.cloud import pubsub_v1
import uuid
import traceback
from bs4 import BeautifulSoup, Comment

def nba_sbr_worker_individual_scraper(event, context):

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

        #game_date = message_data['game_date']
        #game_url_id = message_data['url_id']
        #game_key = message_data['game_key']
        date_formatted = message_data['date_formatted']
        games = message_data['games']

        ##########################################################################
        # Scrape individual games data
        ##########################################################################
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
            ,'Accept-Encoding': 'gzip, deflate, br'
            ,'Accept-Language': 'en-US,en;q=0.9'
            ,'Cache-Control': 'max-age=0'
            ,'Connection': 'keep-alive'
            ,'Cookie': 'user_authenticated=eyJkYXRhIjoie1widXVpZFwiOlwiM2JkYWVkNGYtNzNlMS00YTEyLWEyZTYtMDI5OTIwOGQ5Y2U5XCIsXCJlbmRwb2ludFwiOlwic2JyLW9kZHNcIixcInR5cGVcIjpcImFub255bW91c1wiLFwidWlkXCI6XCIzYmRhZWQ0Zi03M2UxLTRhMTItYTJlNi0wMjk5MjA4ZDljZTlcIn0iLCJ0eXBlIjoib2JqZWN0In0%3D; auth_token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIzYmRhZWQ0Zi03M2UxLTRhMTItYTJlNi0wMjk5MjA4ZDljZTkiLCJqdGkiOiI0MjVkYjMzYS00YzhhLTQ1MGYtOGI2Mi0xYjI5MjVkYmM5N2EiLCJpc3MiOiJTQlIiLCJ0eXBlIjoiQVVUSCIsInVzZXJEYXRhIjoiZXlKMWRXbGtJam9pTTJKa1lXVmtOR1l0TnpObE1TMDBZVEV5TFdFeVpUWXRNREk1T1RJd09HUTVZMlU1SWl3aVpXNWtjRzlwYm5RaU9pSnpZbkl0YjJSa2N5SXNJblI1Y0dVaU9pSmhibTl1ZVcxdmRYTWlmUT09IiwiaWF0IjoxNjMyNjYzMDQzLCJleHAiOjE2MzI2NjY2NDN9.GTksaDsGaD9_KbcCi4OMatUw5oLPWWefTVYliKL-KPWe5BgN2IbLr1defAD9151ILApb5bLmIgYAOceviCc6fw0q0znZUZ7e3_cMJLsMQjMoyYCOSCGW99DFtJny0oDKlBmN7wcMO_maKLjcLcYZYbCrjI835vlxCqbLWhYkbshRWF531HpbGq0oNQoVx5VhpLdkA2kjmAB6aXKgs91VBEDWvudXYisCx5d2Ubmdu1_SIVws8fxmppCk0PqrGGf9TTtw9Q1Kfh0dsDIzkeWVfqUIw5jlfkULz8XCD7nWRWzzGF3IVwUK8TtlDeG4c2flhUCTZbIP6DWmoOY3mxNrug; geo_targeting=eyJkYXRhIjoie1wiZGlkXCI6MixcImNvdW50cnlDb2RlXCI6XCJVU1wifSIsInR5cGUiOiJvYmplY3QifQ%3D%3D; _ga=GA1.2.1472317652.1632663062; _gid=GA1.2.1346335461.1632663062; _cb_ls=1; _cb=B_6crlC3CBRSX2p28; x_geo_cookie_value=US,; _gat_UA-1446389-2=1; _chartbeat2=.1605731739466.1632711478571.0000000000000001.CPaFzUDaHkaNBW3ORSCfadAHBU8JGM.1; _cb_svref=null'
            ,'Host': 'www.sportsbookreview.com'
            ,'If-None-Match': 'W/"d70e6-GhAk1MRXpaZipf9K4YFkmlIENmk"'
            ,'sec-ch-ua': '"Google Chrome";v="93", " Not;A Brand";v="99", "Chromium";v="93"'
            ,'sec-ch-ua-mobile': '?0'
            ,'sec-ch-ua-platform': '"Windows"'
            ,'Sec-Fetch-Dest': 'document'
            ,'Sec-Fetch-Mode': 'navigate'
            ,'Sec-Fetch-Site': 'none'
            ,'Sec-Fetch-User': '?1'
            ,'Upgrade-Insecure-Requests': '1'
            ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
        }


        over_part_id = "15143"
        under_part_id = "15144"
        odds_types = [
                        {"mtid":"83","period_type":"FULL","odds_type":"ML"}
                        ,{"mtid":"401","period_type":"FULL","odds_type":"SPREAD"}
                        ,{"mtid":"402","period_type":"FULL","odds_type":"TOTALS"}

                        ,{"mtid":"91","period_type":"1H","odds_type":"ML"}
                        ,{"mtid":"397","period_type":"1H","odds_type":"SPREAD"}
                        ,{"mtid":"398","period_type":"1H","odds_type":"TOTALS"}

                        ,{"mtid":"168","period_type":"2H","odds_type":"ML"}
                        ,{"mtid":"399","period_type":"2H","odds_type":"SPREAD"}
                        ,{"mtid":"400","period_type":"2H","odds_type":"TOTALS"}

                        ,{"mtid":"93","period_type":"1Q","odds_type":"ML"}
                        ,{"mtid":"403","period_type":"1Q","odds_type":"SPREAD"}
                        ,{"mtid":"407","period_type":"1Q","odds_type":"TOTALS"}
                    ]

        sports_books = [
                        {"paid":"3","sports_book":"5DIMES"}
                        ,{"paid":"9","sports_book":"BOVADA"}
                        ,{"paid":"20","sports_book":"PINNACLE"}
                        ,{"paid":"45","sports_book":"SBR"}
                    ]

        # Get game keys to scrape (calling API for all games within 1 sportsbook)
        game_keys = []
        for g in games:
            game_keys.append(g["game_key"])
        eid_string = ',+'.join(game_keys)
        #eid_string = ',+'+game_key

        # Loop through sports books are create single JSON object to upload to BQ
        lines_to_load = []
        consensus_to_load = []
        cnt = 1
        for sb in sports_books:
            lines_url = "https://www.sportsbookreview.com/ms-odds-v2/odds-v2-service?query=%7B+currentLines(eid:+[" + eid_string + "],+mtid:+[83,+401,+402,+91,+397,+398,+168,+399,+400,+93,+403,+407],+paid:+" + sb['paid'] + ")+openingLines(eid:+[" + eid_string + "],+mtid:+[83,+401,+402,+91,+397,+398,+168,+399,+400,+93,+403,+407],+paid:+" + sb['paid'] + ")+consensus(eid:+[" + eid_string + "],+mtid:+[83,+401,+402,+91,+397,+398,+168,+399,+400,+93,+403,+407])+%7B+eid+mtid+boid+partid+sbid+bb+paid+lineid+wag+perc+vol+tvol+sequence+tim+%7D+maxSequences+%7B+events:+eventsMaxSequence+scores:+scoresMaxSequence+currentLines:+linesMaxSequence+statistics:+statisticsMaxSequence+plays:+playsMaxSequence+consensus:+consensusMaxSequence+%7D+%7D"
            #print(lines_url)
            response = requests.get(lines_url,headers=headers) 
            #print(response.text)
            raw_json = json.loads(response.text)
            #print(raw_json)

            current_lines = raw_json['data']['currentLines']
            opening_lines = raw_json['data']['openingLines']
            consensus = raw_json['data']['consensus']
            
            ######################################################################
            # CURRENT LINES
            for current_line in current_lines:
                opening_line_flag = False
                cur_line = parse_line(current_line, sports_books, odds_types, games, over_part_id, under_part_id,date_formatted,opening_line_flag)
                lines_to_load.append(cur_line)

            ######################################################################
            # OPENING LINES    
            for opening_line in opening_lines:
                opening_line_flag = True
                op_line = parse_line(opening_line, sports_books, odds_types, games, over_part_id, under_part_id,date_formatted,opening_line_flag)
                lines_to_load.append(op_line)

            ######################################################################
            # CONSENSUS
            if cnt == 1:  # Consensus is same across sportsbooks, so only need to save once
                for consensus_raw in consensus:
                    cons = {}
                    # lookup keys
                    game_key = consensus_raw['eid']
                    odds_key = consensus_raw['mtid']
                    team_id = consensus_raw['partid']
            
                    # lookup values
                    ot = next(item for item in odds_types if item["mtid"] == str(odds_key))
                    gt = next(item for item in games if item["game_key"] == str(game_key))
                    if str(team_id) == str(gt["home_team_key"]):
                        h_a = "H"
                        team_abbr = gt["home_team_abbr"]
                        team_city = gt["home_team_city"]
                        team_nickname = gt["home_team_nickname"]
                        o_u = None
                    elif str(team_id) == str(gt["away_team_key"]):
                        h_a = "A"
                        team_abbr = gt["away_team_abbr"]
                        team_city = gt["away_team_city"]
                        team_nickname = gt["away_team_nickname"]
                        o_u = None
                    elif str(team_id) == over_part_id:
                        h_a = None
                        team_abbr = None
                        team_city = None
                        team_nickname = None
                        o_u = "O"
                    elif str(team_id) == under_part_id:
                        h_a = None
                        team_abbr = None
                        team_city = None
                        team_nickname = None
                        o_u = "U"
                    else:
                        raise ValueError("returned team_id (partid) not found in teams api")

                    # Store data
                    cons["game_key"] = game_key
                    cons["game_date"] = date_formatted
                    cons["h_a"] = h_a
                    cons["team_abbr"] = team_abbr
                    cons["team_city"] = team_city
                    cons["team_nickname"] = team_nickname
                    cons["o_u"] = o_u
                    cons["odds_mtid"] = odds_key
                    cons["period_type"] = ot["period_type"]
                    cons["odds_type"] = ot["odds_type"]
                    cons["epoch_timestamp"] = consensus_raw["tim"]
                    cons["wagers_perc"] = consensus_raw["perc"]
                    cons["wagers_count"] = consensus_raw["wag"]
                    cons["load_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    consensus_to_load.append(cons)

            cnt += 1


            ##########################################################################
            # Publish to BigQuery Replication Topic
            ##########################################################################
            #print(lines_to_load)
            #print(consensus_to_load)

            replication_data = {}
            replication_data['bq_dataset'] = 'nba' 
            replication_data['bq_table'] = 'raw_sbr_lines'
            replication_data['data'] = lines_to_load
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))        

            replication_data = {}
            replication_data['bq_dataset'] = 'nba' 
            replication_data['bq_table'] = 'raw_sbr_consensus'
            replication_data['data'] = consensus_to_load
            data_string = json.dumps(replication_data)  
            future = publisher.publish(topic_path, data_string.encode("utf-8"))   

        return f'SportsBookReview.com lines and consensus successfully scraped'

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

            
# Parsing function (same for both open and current)
def parse_line(raw_line, ref_sports_books, ref_odds_types, ref_games, over_part_id, under_part_id, date_formatted, opening_line_flag):

    line = {}
    # lookup keys
    game_key = raw_line['eid']
    odds_key = raw_line['mtid']
    sports_book_key = raw_line['paid']
    team_id = raw_line['partid']

    # lookup values 
    #sb = next(item for item in ref_sports_books if item["paid"] == sports_book_key)
    sb = next(item for item in ref_sports_books if item['paid'] == str(sports_book_key))
    ot = next(item for item in ref_odds_types if item["mtid"] == str(odds_key))
    gt = next(item for item in ref_games if item["game_key"] == str(game_key))
    #print(ref_games)
    #print('@@@@@@')
    #print(gt)
    #print(team_id)
    if str(team_id) == str(gt["home_team_key"]):
        h_a = "H"
        team_abbr = gt["home_team_abbr"]
        team_city = gt["home_team_city"]
        team_nickname = gt["home_team_nickname"]
        o_u = None
    elif str(team_id) == str(gt["away_team_key"]):
        h_a = "A"
        team_abbr = gt["away_team_abbr"]
        team_city = gt["away_team_city"]
        team_nickname = gt["away_team_nickname"]
        o_u = None
    elif str(team_id) == over_part_id:
        h_a = None
        team_abbr = None
        team_city = None
        team_nickname = None
        o_u = "O"
    elif str(team_id) == under_part_id:
        h_a = None
        team_abbr = None
        team_city = None
        team_nickname = None
        o_u = "U"
    else:
        raise ValueError("returned team_id (partid) not found in teams api")

    # Store data
    line["game_key"] = game_key
    line["game_date"] = date_formatted
    line["h_a"] = h_a
    line["team_abbr"] = team_abbr
    line["team_city"] = team_city
    line["team_nickname"] = team_nickname
    line["opening_line_flag"] = opening_line_flag
    line["o_u"] = o_u
    line["odds_mtid"] = odds_key
    line["period_type"] = ot["period_type"]
    line["odds_type"] = ot["odds_type"]
    line["sports_book_key"] = sports_book_key
    line["sports_book"] = sb["sports_book"]
    line["epoch_timestamp"] = raw_line["tim"]
    line["line"] = raw_line["adj"]
    line["odds"] = raw_line["ap"]
    line["load_datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return line