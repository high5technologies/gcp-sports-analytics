import base64
import json
import os
import requests
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup, Comment

game_date = "2018-03-15"

url = 'https://swishanalytics.com/optimus/nba/daily-fantasy-salary-changes?date=' + str(game_date)

r = requests.get(url)
#print(r.content[0:3000])
page_content = r.content
soup = BeautifulSoup(page_content, 'html.parser')
scripts = soup.find_all("script")
script_with_data = ""
is_found = False
for script in scripts:
    if 'this.players_dk' in str(script):
        script_with_data = str(script)
        is_found = True
        break

#if not is_found:
#    throw new exception ....

# Parse HTML to get javascript JSON data objects
dk_base_index = script_with_data.find("this.players_dk")
dk_start = script_with_data.find("[",dk_base_index)
dk_end = script_with_data.find("]",dk_start) + 1
dk_string = script_with_data[dk_start:dk_end]
dk_json = json.loads(dk_string)

fd_base_index = script_with_data.find("this.players_fd")
fd_start = script_with_data.find("[",fd_base_index)
fd_end = script_with_data.find("]",fd_start) + 1
fd_string = script_with_data[fd_start:fd_end]
fd_json = json.loads(fd_string)

# Map JSON - specify columns so new columns doesn't break ingestion
data = []
for record in dk_json:
    d = {}
    d['player_id'] = record['player_id']
    d['player_name'] = record['player_name']
    d['team_abbr'] = record['nickname']
    d['pos_main'] = record['pos_main']
    d['fantasy_pts'] = record['fantasy_pts']
    d['avg_pts'] = record['avg_pts']
    d['fpts_diff'] = record['fpts_diff']
    d['prev_game_date'] = record['date']
    d['salary'] = record['salary']
    d['salary_diff'] = record['salary_diff']
    d['salary_diff_percentage'] = record['salary_diff_percentage']
    d['game_date'] = game_date
    d['salary_source'] = 'dk'
    d['swish_salary_key'] = str(d['salary_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id'])
    d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    data.append(d)

for record in fd_json:
    d = {}
    d['player_id'] = record['player_id']
    d['player_name'] = record['player_name']
    d['team_abbr'] = record['nickname']
    d['pos_main'] = record['pos_main']
    d['fantasy_pts'] = record['fantasy_pts']
    d['avg_pts'] = record['avg_pts']
    d['fpts_diff'] = record['fpts_diff']
    d['prev_game_date'] = record['date']
    d['salary'] = record['salary']
    d['salary_diff'] = record['salary_diff']
    d['salary_diff_percentage'] = record['salary_diff_percentage']
    d['game_date'] = game_date
    d['salary_source'] = 'dk'
    d['swish_salary_key'] = str(d['salary_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id'])
    d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
    data.append(d)

print(data) 
    #print(sk['player_name'])
#print(sk_string)
#print(script_with_data)
#data = json.loads(script.string)

# SK
#{
#  "player_id": "609081",
#  "player_name": "Damion Lee",
#  "nickname": "Hawks",
#  "pos_main": "SG",
#  "fantasy_pts": "14.40",
#  "avg_pts": "22.25",
#  "fpts_diff": "-7.85",
#  "date": "2016-10-19",
#  "salary": "3,200",
#  "salary_diff": "-800",
#  "salary_diff_percentage": "-20.0",
#  "salary_change_html": "<td class=\"width-15 red\" id=\"salary-col\">-$800 (-20.0%)</td>",
#  "salary_change": "-20.0"
#}

# fd
#{
#  "player_id": "608661",
#  "player_name": "Elfrid Payton",
#  "nickname": "Suns",
#  "pos_main": "PG",
#  "fantasy_pts": "31.05",
#  "avg_pts": "29.56",
#  "fpts_diff": "+1.49",
#  "date": "2018-03-13",
#  "salary": "6,400",
#  "salary_diff": "-1500",
#  "salary_diff_percentage": "-19.0",
#  "salary_change_html": "<td class=\"width-15 red\" id=\"salary-col\">-$1500 (-19.0%)</td>",
#  "salary_change": "-19.0"
#}