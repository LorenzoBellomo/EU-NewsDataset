import pandas as pd
import numpy as np
import json
import re
from collections import defaultdict

with open("EU-NewsDataset/topic_modelling/topic_dump_revised.json", 'r') as json_file:
    topics_gt = json.load(json_file)
topics = list(topics_gt.keys())

df = pd.read_csv("EUNewsArticles.csv", index_col=False)
regex = r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b"
topic = None
print("BEFORE: ", len(df))
count = defaultdict(int)
column = []
for url in df.url:
    tmp =  re.findall(regex, url)
    if tmp:
        full_match, domain, topic = tmp[0]
        first = next(filter(lambda x: x in topic, topics), None)
        if first:
            column.append(first)
            count[first] = count[first] + 1
        else:
            column.append(None)
assert len(column) == len(df)
count['before'] = len(df)
count['after'] = len([a for a in column if a])

df['topic'] = column
df.to_csv("EUNewsArticles_w_topics.csv", index=False)
print(count)