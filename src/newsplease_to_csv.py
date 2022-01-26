import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict

rootdir = 'news-please/cc_download_articles/'

with open('datasets/EU_mappings/url2leaning.json', 'r') as json_file:
    leanings = json.load(json_file)


docs = {
    "id": list(),
    "date_publish": list(),
    "maintext": list(),
    "title": list(),
    "source_domain": list(),
    "url": list(), 
    "leaning": list(), 
    "language": list()
}
count = defaultdict(int)
missed = set()
sources = [f.path for f in os.scandir(rootdir) if f.is_dir()]
for s in sources:
    for x in [f for f in os.listdir(s) if os.path.isfile(os.path.join(s, f))]:
        file_path = s +'/' + x
        with open(file_path, 'r') as json_file:
            document = json.load(json_file)
        source = document['source_domain']
        if source not in leanings:
            missed.add(source)
        else:
            docs['id'].append(x)
            docs["date_publish"].append(document['date_publish'])
            docs["maintext"].append(document['maintext'])
            docs["title"].append(document['title'])
            docs["source_domain"].append(source)
            docs["url"].append(document['url'])
            docs["leaning"].append(leanings[source])
            docs["language"].append(document['language'])
        count[source] = count[source] + 1
df = pd.DataFrame(docs)
print(dict(count))
print("==============================================================")
print(list(missed))
with open('test.json', 'w') as json_file:
    json.dump(list(missed), json_file)
#df.to_csv('new_full_dataset.csv')
