import base64
import json
#import os
import requests
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup, Comment

#game_date = '2022-02-03'
game_date = '2018-02-26'
gd = datetime.strptime(game_date, '%Y-%m-%d')

year = gd.strftime("%Y")
month = int(gd.strftime("%m"))
day = int(gd.strftime("%d"))

url_date = str(month) + '_' + str(day) + '_' + str(year)
#print(url_date)
url = 'https://www.fantasylabs.com/api/ownership-contestgroups/2/4/' + url_date + '/'

r = requests.get(url)
json_string = r.content
data_ids = json.loads(json_string)

data = []

for group in data_ids:
    draft_group_id = group['DraftGroupId']

    url = 'https://www.fantasylabs.com/api/contest-ownership/2/' + url_date + '/4/' + str(draft_group_id) + '/0/'
    print(url)
    r = requests.get(url)
    json_string = r.content
    data_json = json.loads(json_string)

    for record in data_json:
        d = {}
        properties = record['Properties']
        d['game_date'] = game_date
        d['dfs_source'] = 'dk'
        d['dfs_contest_id'] = draft_group_id
        d['fantasy_result_id'] = properties['FantasyResultId']
        d['player_id'] = properties['PlayerId']
        d['player_name'] = properties['Player_Name']
        d['position'] = properties['Position']
        d['team'] = properties['Team']
        d['salary'] = properties['Salary']
        d['actual_points'] = properties['ActualPoints']
        d['ownership_average'] = properties['Average']
        d['ownership_volatility'] = properties['Volatility']
        d['gpp_grade'] = properties['GppGrade']
        d['fantasylabs_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
        d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        data.append(d)

  

#print(data)