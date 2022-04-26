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
import urllib.request

def nba_sbr_worker_Schedule_scraper(event, context):

    # Config
    url = "http://metadata.google.internal/computeMetadata/v1/project/project-id"
    req = urllib.request.Request(url)
    req.add_header("Metadata-Flavor", "Google")
    project_id = urllib.request.urlopen(req).read().decode()
    topic_id = "nba_sbr_games_to_scrape"
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project_id, topic_id)
    
    ##########################################################################
    # Scrape schedule of games
    ##########################################################################
    
    try:
    
        # Get Mesage
        pubsub_message = base64.b64decode(event['data']).decode('utf-8')
        message_data = json.loads(pubsub_message)

        date_string = message_data['date_string']
        date_formatted = message_data['date_formatted']

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
        
        url = "https://www.sportsbookreview.com/betting-odds/nba-basketball/?date=" + date_string
        print(url)
        r = requests.get(url,headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        # Get all script nodes
        scripts  = soup.find_all('script')

        # Loop through list
        for script in scripts:
            
            # Find list with data
            if "window.__INITIAL_STATE__=" in str(script):
                
                json_parsed = str(script).split("window.__config")[0].rstrip()[:-1].split("window.__INITIAL_STATE__=")[1].lstrip()
                #json_string = "'" + str(json_parsed) + "'"
                json_string = json_parsed
                print(json_string[0:100])
                data = json.loads(json_string)
                events = data["events"]["events"]
                event_keys = list(events.keys())

                #games = []
                for key in event_keys:
                    #print(key)
                    game = {}
                    game["game_key"] = key
                    #game["date_formatted"] = date_formatted
                    participants = events[key]["participants"]
                    participant_keys = list(participants.keys())
                    for participant_key in participant_keys:
                        node = events[key]["participants"][participant_key]
                        # Example Participant name
                        #{"1160":{"eid":3871416,"partid":1160,"partbeid":5963802,"psid":1160,"ih":true,"rot":538,"tr":null,"sppil":null,"sppic":null,"startingPitcher":null,"source":{"tmid":1160,"lid":5,"tmblid":275526,"nam":"Washington","nn":"Wizards","sn":"Washington","abbr":"WAS","cit":"Washington","senam":"2020-21","imageurl":"https:\u002F\u002Flogos.sportsbookreview.com\u002Flogos-original\u002Fb95de91f-7ed9-4d7e-8544-7b3e104532e0-original.PNG"}}

                        if node["ih"]:
                            game["home_team_key"] = participant_key
                            game["home_team_city"] = node["source"]["cit"]
                            game["home_team_nickname"] = node["source"]["nn"]
                            game["home_team_abbr"] = node["source"]["abbr"]
                            game["season"] = node["source"]["senam"]
                        else:
                            game["away_team_key"] = participant_key
                            game["away_team_city"] = node["source"]["cit"]
                            game["away_team_nickname"] = node["source"]["nn"]
                            game["away_team_abbr"] = node["source"]["abbr"]
                    games = []
                    games.append(game)


                    msg = {}
                    msg['date_formatted'] = date_formatted
                    msg['games'] = games
                    data_string = json.dumps(msg)  
                    future = publisher.publish(topic_path, data_string.encode("utf-8"))        

                #print(games)
                break

        return f'SportsBookReview.com schedule successfully scraped'

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

            