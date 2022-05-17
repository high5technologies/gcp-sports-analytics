import os 
import json

dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
file_name = 'data.json'
text_file = open(os.path.join(dir,file_name), "r")

#read whole file to a string
data = text_file.read()

#print(data)

json_strings = data.decode().split('\n')

for json_string in json_strings:
    json_data = json.loads(json_string)
    print(json_data)
