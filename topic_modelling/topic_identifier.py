import re
import json
from collections import defaultdict
import numpy as np

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")

with open('url_id_mapping.json', 'r') as json_file:
    mapping = json.load(json_file)
lowercase = {a: b.lower() for a, b in mapping}
print(len(lowercase))

unique_1, unique_2 = defaultdict(int), defaultdict(int)
for k, v in lowercase.items():  
    tmp = re.findall(regex, v)
    for full_match, url, topic in tmp:
        #print(full_match, "----------------", topic) #www.aaaaa.it/1/2/3
        #url, topic = x.groups()
        if topic:
            split = topic.split("/")
            #print(split)
            if len(split) > 3:
                unique_1[split[2]] = unique_1[split[2]] + 1
                unique_2[split[2]] = unique_2[split[2]] + 1
            if len(split) > 4:
                unique_2[split[3]] = unique_2[split[3]] + 1

#print("MAX ", max(unique_2.values()), "AVG", sum(unique_2.values())/len(unique_2.values()))
unique_1 = [k for k, v in unique_1.items() if v > 500]
unique_2 = [k for k, v in unique_2.items() if v > 500]
print("LENGTH UNIQUE 1", len(unique_1))
print("LENGTH UNIQUE 2", len(unique_2))

with open('unique1_500.json', 'w') as json_file:
    json.dump(list(unique_1), json_file)
with open('unique2_500.json', 'w') as json_file:
    json.dump(list(unique_2), json_file)

print(len(lowercase))