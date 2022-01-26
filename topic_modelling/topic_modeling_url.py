import pandas as pd
import numpy as np
import json
import re

#bulgaro
list_ = ['politic', 'politik', 'poliitika', 'politiikka', 'politique', 'politik', 'polityka']

with open('url_id_mapping.json', 'r') as json_file:
    mapping = json.load(json_file)

lowercase = {a: b.lower() for a, b in mapping}

#CASES
filtered = [a for a, b in lowercase.items() if any(word in b for word in list_)]
print("BEFORE: ", len(lowercase), "- AFTER,", len(filtered))

with open('url_id_mapping_filtered.json', 'w') as json_file:
    json.dump(filtered, json_file)