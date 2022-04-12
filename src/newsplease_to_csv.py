import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict

rootdir = 'news-please/cc_download_articles/'

with open('EU-NewsDataset/mappings/url2leaning.json', 'r') as json_file:
    leanings = json.load(json_file)

tmp = {}
for s, l in leanings.items():
    if s.startswith('www.'):
        tmp[s[4:]] = l
leanings.update(tmp)

count = defaultdict(int)
missed = set()
sources = [f.path for f in os.scandir(rootdir) if f.is_dir()]
i = 0
for s in sources:
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
    for x in [f for f in os.listdir(s) if os.path.isfile(os.path.join(s, f))]:
        file_path = s +'/' + x
        with open(file_path, 'r') as json_file:
            document = json.load(json_file)
        source = document['source_domain']
        if source not in leanings:
            missed.add(source)
            break
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
    if len(docs['id']) > 0:
        df = pd.DataFrame(docs)
        path_ = "final_dataset/" + source + ".csv"
        df.to_csv(path_, index=False)
        print("DONE ", source, " - len =", len(df), " - ", i, " out of", len(sources), " SOURCES")
    else:
        print("EMPTY ", source, " - ", i, " out of", len(sources), " SOURCES")
    i = i + 1
with open('count.json', 'w') as json_file:
    json.dump(count, json_file)
with open('missed.json', 'w') as json_file:
    json.dump(list(missed), json_file)
