import pandas as pd
import numpy as np
from bertopic import BERTopic
import random
import re
import json

with open('tmp_topic_url/url_id_mapping.json', 'r') as json_file:
    lowercase = {a: b.lower() for a, b in json.load(json_file)}
len(lowercase)

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")
regex_num = re.compile(r"\b[0-9]+(?:\.html)?\b")

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

keys = random.sample(list(lowercase.keys()), 100000)
documents = {a: cleanup(b) for a, b in lowercase.items() if a in keys}

topic_model = BERTopic(language="multilingual", n_gram_range=(1,2), min_topic_size=100, nr_topics=50, calculate_probabilities=False, low_memory=True)
topics, probs = topic_model.fit_transform(documents.values())


freq = topic_model.get_topic_info()
print(freq)

fig = topic_model.visualize_barchart(height=700)
fig.write_html("topic_dump/barchart.html")

fig = topic_model.visualize_term_rank(log_scale=True)
fig.write_html("topic_dump/term_rank.html")

fig = topic_model.visualize_topics()
fig.write_html("topic_dump/topics.html")

fig = topic_model.visualize_hierarchy(width=800)
fig.write_html("topic_dump/hierarchy.html")

fig = topic_model.visualize_heatmap()
fig.write_html("topic_dump/heatmap.html")