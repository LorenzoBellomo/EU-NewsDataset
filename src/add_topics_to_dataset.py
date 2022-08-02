import pandas as pd
import json

df = pd.read_csv("EUNewsArticles_translated_topics.csv")
with open('EU-NewsDataset/notebooks/all_topic_mapped.json', 'r') as json_file:
    topics = json.load(json_file)

planet = {
    'www.corriere.it': 'environment', 
    'www.lalibre.be': 'environment', 
    'www.lemonde.fr': None, 
    'www.liberation.fr': 'article_type:world', 
    'www.real.gr': 'environment',
}

city = {
    'www.dn.pt': "article_type:local",
    'www.hs.fi': "article_type:local",
    'www.theguardian.com': "city",
    'joop.bnnvara.nl': None, 
    'www.eldiario.es': None, 
    'www.express.co.uk': None, 
    'www.kathimerini.gr': "city",
    'www.krytykapolityczna.pl': "city",
}


article_type_1, article_type_2, article_type_grp_list = [], [], []
topic_1, topic_2, topic_grp_list = [], [], []
missing = {'city': set(), 'planet': set()}
for t1, t2, domain in zip(df.translated_tag1, df.translated_tag2, df.source_domain):
    topic_grp, article_type_grp = '', ''
    handle = [(1, t1), (2, t2)]
    for i, t in handle:
        topic, article_type = None, None
        if t == 'planet':
            topic = planet[domain]
        elif t == 'city':
            topic = city[domain]
        elif t in topics and topics[t]:
            if topics[t].startswith("article_type"):
                article_type = topics[t]
            else:
                topic = topics[t]
        if i == 1:
            topic_1.append(topic)
            article_type_1.append(article_type)
            if topic:
                topic_grp = topic
            if article_type:
                article_type_grp = article_type
        if i == 2:
            topic_2.append(topic)
            article_type_2.append(article_type)
            if topic:
                if topic_grp:
                    if topic != topic_grp:
                        topic_grp = topic_grp + '_' + topic
                else:
                    topic_grp = topic
            if article_type:
                if article_type_grp:
                    if article_type != article_type_grp:
                        sss = article_type.split(':')[1]
                        article_type_grp = article_type_grp + '_' + sss
                else:
                    article_type_grp = article_type
    if topic_grp:
        topic_grp_list.append(topic_grp)
    else:
        topic_grp_list.append(None)
    if article_type_grp:
        article_type_grp_list.append(article_type_grp)
    else:
        article_type_grp_list.append(None)


df['assigned_topic1'] = topic_1
df['assigned_topic2'] = topic_2
df['topic'] = topic_grp_list
df['article_type1'] = article_type_1
df['article_type2'] = article_type_2
df['article_type'] = article_type_grp_list

df.to_csv("EUNewsArticles_updated_topics.csv", index=False)
