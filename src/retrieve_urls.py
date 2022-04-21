from googlesearch import search
import json
import pandas as pd
import numpy as np

def cleanup(s):
    if s.startswith('www.'):
        return s[4:]
    return s

with open("EU-NewsDataset/mappings/url2leaning.json", 'r') as json_file:
    leanings = json.load(json_file)

tmp = leanings.copy()
for s, l in tmp.items():
    if s.startswith('www.'):
        leanings[s[4:]] = l
        del leanings[s]
domains = leanings.keys()

#df = pd.read_csv("BiasClassification/data/eudata_without_url.csv", index_col=False)
#data = {"title": list(df.title)[:100], "source_domain": list(df.source_domain)[:100], "id": list(df['id'])[:100]}
#df_ = pd.DataFrame(data)
#df_.to_csv("tmp.csv")
df_ = pd.read_csv("tmp.csv", index_col=False)
mapping = {}
print("START")
i = 0
for t, d, id_ in zip(df_.title, df_.source_domain, df_['id']):
    i = i + 1
    print(i)
    q = str(d) + " " + str(t)
    res = list(search(q, num=1, pause=2))[0]
    to_ret = list(res)[0]
    if any([x for x in domains if x in to_ret]):
        mapping[id_] = to_ret
print(len(mapping))
print("DONE")