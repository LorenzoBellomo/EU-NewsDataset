import pandas as pd
import numpy as np
from bertopic import BERTopic
import random
import re
import json

def cleanup(t):
    tmp = re.findall(regex, t)
    if len(tmp[0]) == 3:
        t = tmp[0][2]
        t = t.replace("/", " ")
        t = t.replace("_", " ")
        t = t.replace("-", " ")
        t = t.replace("%20", " ")
        t = re.sub(regex_num, '', t)
        return t

with open('tmp_topic_url/url_id_mapping.json', 'r') as json_file:
    lowercase = {a: b.lower() for a, b in json.load(json_file)}
len(lowercase)

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")
regex_num = re.compile(r"\b[0-9]+(?:\.html)?\b")

keys = random.sample(list(lowercase.keys()), 100000)
documents = {a: cleanup(b) for a, b in lowercase.items() if a in keys}

targets = ['sport', 'politics', 'news', 'tech', 'economy', 'society', 'environment', 'science', 'brexit', 'opinion']

topic_model = BERTopic(verbose=True, language="multilingual", n_gram_range=(1,2), calculate_probabilities=False, low_memory=True)
topics, _ = topic_model.fit_transform(documents.values(), y=targets)

print(topic_model.get_topic_info())

fig = topic_model.visualize_barchart(height=700)
fig.write_html("topic_dump/supervised/barchart.html")

fig = topic_model.visualize_term_rank(log_scale=True)
fig.write_html("topic_dump/supervised/term_rank.html")

fig = topic_model.visualize_topics()
fig.write_html("topic_dump/supervised/topics.html")

fig = topic_model.visualize_hierarchy(width=800)
fig.write_html("topic_dump/supervised/hierarchy.html")

fig = topic_model.visualize_heatmap()
fig.write_html("topic_dump/supervised/heatmap.html")