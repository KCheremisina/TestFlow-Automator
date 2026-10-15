import json

JUNK_KEYS = {
    'fields',
    'created_at',
    'updated_at',
    'created_by',
    'updated_by',
    'attachments',
    'comments',
    'custom_fields',
    'history',
    'links',
    'tags',
    'responsible',
    'preconditions',
    'info',
    'date',
    'execution_time',
    'planned_update',
    'params',
    'author',
    'labels'
}

def is_empty_value(val):
    return val == "" or val is None or val == [] or val == {}

def remove_junk(obj):
    if isinstance(obj, dict):
        cleaned = {}
        for k, v in obj.items():
            if k in JUNK_KEYS or is_empty_value(v):
                continue
            
            cleaned[k] = remove_junk(v)
        return cleaned
        
    elif isinstance(obj, list):
        return [remove_junk(item) for item in obj]
        
    else:
        return obj

INPUT_FILE = 'qwe.json'   
OUTPUT_FILE = 'qwe1.json'   

print(f"Загружаю {INPUT_FILE}...")
with open(INPUT_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("...")
cleaned_data = remove_junk(data)

with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
    json.dump(cleaned_data, f, indent=2, ensure_ascii=False)

print("велдан")