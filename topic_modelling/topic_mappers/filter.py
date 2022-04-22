import json

with open("topic_dump_revised.json", 'r') as json_file:
    rev = json.load(json_file)

rev_l = list()
for v in rev.values():
    rev_l = rev_l + list(v)

with open("topic_dump.json", 'r') as json_file:
    dump = json.load(json_file)

new_dump = {k: list() for k in dump.keys()}
for k, v in dump.items():
    for x in v:
        if x not in rev_l:
            new_dump[k].append(x)
            rev_l.append(x)

with open("topic_dump.json", 'w') as json_file:
    json.dump(new_dump, json_file)

with open("unique_500.json", 'r') as json_file:
    unique = json.load(json_file)

unique_ = []
for x in unique:
    if x not in rev_l:
        unique_.append(x)
        rev_l.append(x)
with open("unique_500.json", 'w') as json_file:
    json.dump(unique_, json_file)

with open("unique_50.json", 'r') as json_file:
    unique = json.load(json_file)

unique_ = []
for x in unique:
    if x not in rev_l:
        unique_.append(x)
        rev_l.append(x)
with open("unique_50.json", 'w') as json_file:
    json.dump(unique_, json_file)
