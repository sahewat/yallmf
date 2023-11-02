import json

def load_jsonl(path):
    json_lines_raw = open(path).readlines()
    json_lines = [json.loads(line) for line in json_lines_raw]
    return json_lines

