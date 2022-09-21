import json
  
# Opening JSON file
f = open('c:/Code/Hi5/gcp-sports-analytics/sandbox/nba/data.json')

f_string = str(f.read())

g = f_string.replace("'",'"')
g = g.replace(" ","").replace('\r', '').replace('\n', '')
g = g.replace('{','{"')
g = g.replace('}','"}')
g = g.replace(':','":"')
g = g.replace(',','","')
g = g.replace('""','"')
g = g.replace(':"[',':[')
g = g.replace(']","','],')
g = g.replace('}","','},')
g = g.replace('},]','}]')
g = g.replace('],}',']}')
#print(g)
data = json.loads(g)
for key in data.keys():
    arr = data[key]
    for record in arr:
        

#f.close()