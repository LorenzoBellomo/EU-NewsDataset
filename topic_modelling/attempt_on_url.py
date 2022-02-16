import re
import json
from collections import defaultdict
import numpy as np
from bertopic import BERTopic

regex = re.compile(r"\b((?:https?:\/\/)?(?:(?:www\.)?((?:[\da-z\.-]+)\.(?:[a-z]{2,6})))((?:\/[\w\.-]*)*\/?))\b")

with open('url_id_mapping.json', 'r') as json_file:
    mapping = json.load(json_file)
lowercase = {a: b.lower() for a, b in mapping}
print(len(lowercase))

docs = []
for k, v in lowercase.items():  
    tmp = re.findall(regex, v)
    for full_match, url, topic in tmp:
        if topic:
            docs.append(topic)

topic_model = BERTopic(language="multilingual", calculate_probabilities=True, verbose=True)
topics, probs = topic_model.fit_transform(docs)

freq = topic_model.get_topic_info()
print(list(freq.Name))