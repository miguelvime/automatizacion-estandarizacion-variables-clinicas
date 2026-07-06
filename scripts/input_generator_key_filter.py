import json
import os 

json_to_be_filtered_path = 'data/raw_id_cif/input_of_generator_extra_info.json'
filtered_json_path = 'data/raw_id_cif/input_of_generator_id_icf.json'
key_1 = 'id_code_combination'
key_2 = 'icf_code'

def filter_json_keys(json_to_be_filtered_path,filtered_json_path,key_1,key_2):
    
    with open(json_to_be_filtered_path,'r',encoding='utf-8') as json_to_be_filtered_file:
        data = json.load(json_to_be_filtered_file) 

    filtered_list_of_objects = [] 

    for item in data: 
            filtered_item = {}
            if key_1 in item:
                filtered_item[key_1] = item[key_1]
            if key_2 in item:
                filtered_item[key_2] = item[key_2]
            
            filtered_list_of_objects.append(filtered_item)
        
    os.makedirs(os.path.dirname(filtered_json_path), exist_ok=True)

    with open (filtered_json_path,'w', encoding='utf-8') as filtered_json_file:
        json.dump(filtered_list_of_objects, filtered_json_file, indent=4) 

    return len(filtered_list_of_objects) 

filtered_count = filter_json_keys(json_to_be_filtered_path, filtered_json_path, 'id_code_combination', 'icf_code')
print(f"Process complete: Successfully extracted {filtered_count} objects with keys ('id_code_combination' and 'icf_code') to {filtered_json_path}")
    
