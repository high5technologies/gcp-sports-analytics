import base64
import json
#import os
import requests
from datetime import datetime, timedelta, date
from bs4 import BeautifulSoup, Comment

def format_js_object(g):
    g = g.replace("'",'"')
    g = g.replace(" ","").replace('\r', '').replace('\n', '')
    g = g.replace('{','{"')
    g = g.replace('}','"}')
    g = g.replace(':','":"')
    g = g.replace(',','","')
    g = g.replace(':"[',':[')
    g = g.replace(']","','],')
    g = g.replace('}","','},')
    g = g.replace('""','"')
    g = g.replace('},]','}]')
    g = g.replace('],}',']}')
    g = g.replace('],"}',']}')
    g = g.replace('{"}','{}')
    return g

def extract_json_string_from_html(html, find_string):
    base_index = html.find(find_string)
    start = html.find("{",base_index)
    end = html.find(";",start)
    json_string = html[start:end]
    json_string = format_js_object(json_string)
    return json_string


url = 'https://www.linestarapp.com/DesktopModules/DailyFantasyApi/API/Fantasy/GetPeriodInformation?getLineupCnt=true&periodId=1&site=2&sport=2'

r = requests.get(url)
#print(r.content[0:3000])
json_string = r.content

data = json.loads(json_string)

pid = data['Info']['Periods'][0]['Id']
pid = 1755 # override
dfs_source = 'FanDuel'

url = 'https://www.linestarapp.com/Ownership/Sport/NBA/Site/' + dfs_source + '/PID/' + str(pid)

r = requests.get(url)
#print(r.content[0:3000])
page_content = r.content
soup = BeautifulSoup(page_content, 'html.parser')
scripts = soup.find_all("script")
script_with_date_field = ""
script_with_data = ""
data = []

#################################################
# Extract Game Date (since all we get is the PID)
is_found = False
for script in scripts:
    if 'fscInfo' in str(script):
        script_with_date_field = str(script)
        is_found = True
        break

base_index = script_with_date_field.find('fscInfo')
base_index_2 = script_with_date_field.find("periodName",base_index)
start = script_with_date_field.find('"',base_index) + 1
end = script_with_date_field.find('",',start)
game_date_string = script_with_date_field[start:end]
game_date = datetime.strptime(game_date_string, '%b %d, %Y')

#################################################
# Find Data
is_found = False
for script in scripts:
    if 'projectedSlatesDict' in str(script):
        script_with_data = str(script)
        is_found = True
        break

# Projected
projected_json_string = extract_json_string_from_html(script_with_data,'projectedSlatesDict')
#print(projected_json_string)
projected_json = json.loads(projected_json_string)

for key in projected_json.keys():
    arr = projected_json[key]
    for record in arr:
        d = {}
        d['game_date'] = game_date
        d['pid'] = pid
        d['dfs_source'] = dfs_source
        d['dfs_contest_id'] = key
        d['linestar_type'] = 'projected'
        d['player_id'] = record['id']
        d['player_name'] = record['name']
        d['owned'] = record['owned']
        d['player_pos'] = record['pos']
        d['team'] = record['team']
        d['player_salary'] = record['sal']
        d['linestar_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
        d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        data.append(d)


# Actual
actual_json_string = extract_json_string_from_html(script_with_data,'actualResultsDict')
actual_json = json.loads(actual_json_string)

for key in actual_json.keys():
    arr = actual_json[key]
    for record in arr:
        d = {}
        d['game_date'] = game_date
        d['pid'] = pid
        d['dfs_source'] = dfs_source
        d['dfs_contest_id'] = key
        d['linestar_type'] = 'actual'
        d['player_id'] = record['id']
        d['player_name'] = record['name']
        d['owned'] = record['owned']
        d['player_pos'] = record['pos']
        d['team'] = record['team']
        d['player_salary'] = record['sal']
        d['linestar_key'] = str(d['dfs_source']) + '|' + str(d['game_date']) + '|' + str(d['player_id']) + '|' + str(d['dfs_contest_id'])
        d['load_datetime'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
        data.append(d)

print(data)
#projected_base_index = script_with_data.find("projectedSlatesDict")
#projected_start = script_with_data.find("{",projected_base_index)
#projected_end = script_with_data.find(";",projected_start)
#projected_string = script_with_data[projected_start:projected_end]
#projected_string = format_js_object(projected_string)
#projected_json = json.loads(projected_string)

# bad
#print(projected_string)
#projected_json = json.loads(projected_string.strip().replace("'",'"'))




#    print(projected_json[key])
#print(projected_json[0])
#print(projected_string)

#data = json.loads(g)
#for key in data.keys():
#    arr = data[key]
#    for record in arr:


