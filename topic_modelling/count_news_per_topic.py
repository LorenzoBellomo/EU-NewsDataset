import pandas as pd
import numpy as np
import random
import re
import json
from collections import defaultdict

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
    else:
        print("ERROR")

def assign_topic(t, gt_words):
    return next((w for w in gt_words if w in t), -1)

with open('../mappings/url_id_mapping.json', 'r') as json_file:
    lowercase = {a: b.lower() for a, b in json.load(json_file)}

with open('../mappings/url2leaning.json', 'r') as json_file:
    leanings = json.load(json_file)

to_add = {}
for k, v in leanings.items():
    if k.startswith('www.'):
        to_add[k[4:]] = v
    else:
        to_add['www.' + k] = v
leanings.update(to_add)

per_class = defaultdict(int)

with open('topics_by_url/topic_dump_revised.json', 'r') as json_file:
    ground_truth = json.load(json_file)
rev_gt = {}
for k, v in ground_truth.items():
    for x in v:
        rev_gt[x] = k 
        
gt_words = list(ground_truth.keys())

documents = {a: cleanup(b) for a, b in lowercase.items()}
indices = {label: i for i, label in enumerate(gt_words)}
rev_idx = {i: label for label, i in indices.items()}
new_labels = [indices.get(assign_topic(v, gt_words), -1) for v in documents.values()]
counts = defaultdict(int)
for i, u in zip(new_labels, lowercase.values()):
    if i != -1:
        counts[rev_idx[i]] = counts[rev_idx[i]] + 1
        if rev_idx[i] == 'politics':
            tmp = re.findall(regex, u)
            per_class[leanings[tmp[0][1]]] = per_class[leanings[tmp[0][1]]] + 1

print(dict(counts))
print(dict(per_class))
print("OTHERS are:", len(lowercase) - sum(list(counts.values())))