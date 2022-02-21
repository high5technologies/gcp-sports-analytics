import json
import os

file_name = 'data.json'
#file_name = 'json_to_parse.json'
dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
with open(os.path.join(dir,file_name)) as f:
    data = json.load(f)
f.close()

print(data)

def iterdict(d, base_key, nested_path, source_name, target_name, tab_index):
    #print(type(d))
    # check types and iterate for nested
    if isinstance(d, dict):
        
        for k,v in d.items(): 
            # concat key for nested
            nk = base_key + ('' if base_key == '' else '_') + str(k)

            # nested path
            if nested_path == '':
                np = str(source_name) + '["' + str(k) + '"]'
            else:
                np = str(nested_path) + '["' + str(k) + '"]'

            iterdict(v, nk, np, source_name, target_name, tab_index)

    elif isinstance(d,list):
        print_string = create_tab_string(tab_index) + 'for itm' + str(tab_index + 1) + ' in ' + nested_path + ':'
        print(print_string)
        tab_index += 1
        for i in d:
            iterdict(i, base_key, 'itm' + str(tab_index), 'itm' + str(tab_index), str(target_name) + str(base_key), tab_index)
        tab_index -= 1

    else:            
        #print (nk,":::",v)
        print_string = create_tab_string(tab_index) + str(target_name) + '["' + base_key + '"] = ' + nested_path
        print(print_string)

    
    
    


def create_tab_string(tab_index):
    tab_string = ''
    for x in range(tab_index):
        tab_string += '\t'
        #print(tab_index)
    return tab_string

#iterdict(data,'','','source_data','data_to_load',0)

#a = {'z': {10: {1: 2, 3: 4}, 20: {5: 6}, 30: [{'a':'b'},{'c':'d'},{'e':'f'},{'g': [{'aa':'bb'},{'cc':'dd'},{'ee':'ff'}]}]}}
#iterdict(a,'','','source_data','data_to_load',0)





