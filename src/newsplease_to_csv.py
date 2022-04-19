import pandas as pd
import numpy as np
import json
import os
from collections import defaultdict
from itertools import dropwhile
import ray

ray.init()
@ray.remote
def create_csv(s, i):
    print("DOING ", s, " - ", i, " out of", len(left_sources), " SOURCES")
    spl_ = s.split("/")
    sssss = spl_[len(spl_) - 1]
    if sssss not in leanings:
        return sssss
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

        docs['id'].append(x)
        docs["date_publish"].append(document['date_publish'])
        docs["maintext"].append(document['maintext'])
        docs["title"].append(document['title'])
        docs["source_domain"].append(source)
        docs["url"].append(document['url'])
        docs["leaning"].append(leanings[source])
        docs["language"].append(document['language'])

    if len(docs['id']) > 0:
        df = pd.DataFrame(docs)
        path_ = "final_dataset/" + source + ".csv"
        df.to_csv(path_, index=False)
        print("DONE ", source, " - len =", len(df), " - ", i, " out of", len(left_sources), " SOURCES")
    else:
        print("EMPTY ", source, " - ", i, " out of", len(left_sources), " SOURCES")

rootdir = 'news-please/cc_download_articles/'

with open('EU-NewsDataset/mappings/url2leaning.json', 'r') as json_file:
    leanings = json.load(json_file)

reached_s = "peric.blog.sme.sk"

tmp = {}
for s, l in leanings.items():
    if s.startswith('www.'):
        tmp[s[4:]] = l
leanings.update(tmp)

sources = [f.path for f in os.scandir(rootdir) if f.is_dir()]
left_sources = list(dropwhile(lambda x: reached_s not in str(x), sources))
print("MISSING", len(left_sources), "SOURCES")
futures = [create_csv.remote(s, i) for i, s in enumerate(left_sources)]
missed = ray.get(futures)

with open('missed.json', 'w') as json_file:
    json.dump(list(missed), json_file)