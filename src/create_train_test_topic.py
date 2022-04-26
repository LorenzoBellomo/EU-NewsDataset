import pandas as pd 
import numpy as np
import random
import json

df = pd.read_csv("EUNewsArticles_w_topics.csv", index_col=False)
df = df[df['topic'].notna()]
sizes = {k: len(df[df['topic'] == k]) for k in np.unique(df.topic)}
print(sizes)
min_size = min(sizes.values())
print(min_size)

done = False
df_ = pd.DataFrame()
while not done:
    new_sizes = {}
    for k in sizes.keys():
        filt = df[df['topic'] == k]
        print(min_size, " - ", len(filt))
        tmp = filt.sample(min(min_size, len(filt)))
        df_ = pd.concat([df_, tmp], ignore_index=True)
        new_sizes[k] = {d: len(tmp[tmp['source_domain'] == d]) for d in np.unique(tmp.source_domain)}
    print(new_sizes)
    with open("sizes.json", 'w') as json_file:
        json.dump(new_sizes, json_file)
    if input("OK?") == 'y':
        done = True

df_.drop_duplicates(inplace=True)
df_.to_csv("topic_modelling_traning_test.csv", index=False)