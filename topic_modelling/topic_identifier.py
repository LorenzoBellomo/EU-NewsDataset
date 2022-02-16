import re
import json
from collections import defaultdict
import numpy as np

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")

with open('url_id_mapping.json', 'r') as json_file:
    mapping = json.load(json_file)
lowercase = {a: b.lower() for a, b in mapping}
print(len(lowercase))

unique = defaultdict(int)
for k, v in lowercase.items():  
    tmp = re.findall(regex, v)
    for full_match, url, topic in tmp:
        #print(full_match, "----------------", topic) #www.aaaaa.it/1/2/3
        #url, topic = x.groups()
        if topic:
            split = topic.split("/")
            for i, s in enumerate(split):
                if i > 0 and i < len(split) - 1:
                    unique[split[i]] = unique[split[i]] + 1

#print("MAX ", max(unique_2.values()), "AVG", sum(unique_2.values())/len(unique_2.values()))
unique_500 = [k for k, v in unique.items() if v > 500]
unique_50 = [k for k, v in unique.items() if v > 50]
print("LENGTH UNIQUE 500", len(unique_500))
print("LENGTH UNIQUE 50", len(unique_50))

with open('unique_500.json', 'w') as json_file:
    json.dump(list(unique_500), json_file)
with open('unique2_50.json', 'w') as json_file:
    json.dump(list(unique_50), json_file)