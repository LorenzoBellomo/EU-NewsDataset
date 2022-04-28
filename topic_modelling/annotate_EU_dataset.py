import pandas as pd
import numpy as np
import json
import re
from collections import defaultdict

with open("EU-NewsDataset/topic_modelling/topic_mappers/topic_dump_revised.json", 'r') as json_file:
    topics_gt = json.load(json_file)
topics = list(topics_gt.keys())
rev_topics = {}
for k, v in topics_gt.items():
    for x in v:
        rev_topics[x] = k
words = list(rev_topics.keys())
words.remove("coronavirus")
words.remove("koronawirus-sars-cov-2")
words.append("coronavirus")
words.append("koronawirus-sars-cov-2")
covid_words = ['coronavirus', 'covid', 'sars-cov-2']

df = pd.read_csv("EUNewsArticles.csv", index_col=False)
regex = r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b"
topic = None
print("BEFORE: ", len(df))
count = defaultdict(int)
column, detected = [], []
for url in df.url:
    tmp =  re.findall(regex, url)
    x = None
    y = None
    if tmp:
        full_match, domain, topic = tmp[0]
        if topic:
            split = topic.split("/")
            for s in split:
                if not x and s in words:
                    x = rev_topics[s]
                    y = s
            if not x:
                if any([a in topic for a in covid_words]):
                    x = "coronavirus"
                    y = next(filter(lambda x: x in topic, covid_words), None)
    column.append(x)
    detected.append(y)
    count[x] = count[x] + 1
assert len(column) == len(df)
count['before'] = len(df)
count['after'] = len([a for a in column if a])

df['topic'] = column
df['topic_word'] = detected
df.to_csv("EUNewsArticles_w_topics.csv", index=False)
print(count)