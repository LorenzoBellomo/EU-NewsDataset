import pandas as pd
import numpy as np
from bertopic import BERTopic
import random
import re
import json
from collections import defaultdict

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

def assign_topic(t, gt_words):
    return next((w for w in gt_words if w in t), -1)


with open('tmp_topic_url/url_id_mapping.json', 'r') as json_file:
    lowercase = {a: b.lower() for a, b in json.load(json_file)}

with open('tmp_topic_url/topic_dump_revised.json', 'r') as json_file:
    ground_truth = json.load(json_file)
    rev_gt = {}
    for k, v in ground_truth.items():
        for x in v:
            rev_gt[x] = k 
    gt_words = list(rev_gt.keys())

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")
regex_num = re.compile(r"\b[0-9]+(?:\.html)?\b")

keys = random.sample(list(lowercase.keys()), 100000)
documents = {a: cleanup(b) for a, b in lowercase.items() if a in keys}
indices = {label: i for i, label in enumerate(gt_words)}
rev_idx = {i: label for label, i in indices.items()}
new_labels = [indices.get(assign_topic(v, gt_words), -1) for v in documents.values()]
counts = defaultdict(int)
for i in new_labels:
    if i != -1:
        counts[rev_idx[i]] = counts[rev_idx[i]] + 1
print(dict(counts))
print("OTHERS are:", 100000 - sum(list(counts.values())))

topic_model = BERTopic(verbose=True, language="multilingual", n_gram_range=(1,2), calculate_probabilities=False, low_memory=True, nr_topics=50)
topics, _ = topic_model.fit_transform(documents.values(), y=new_labels)

print(topic_model.get_topic_info())

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