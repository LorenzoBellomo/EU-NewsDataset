import pandas as pd
import numpy as np
import json
import random 

from langdetect import detect
from matplotlib import pyplot as plt

from contextualized_topic_models.models.ctm import ZeroShotTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessing
import nltk

import os
# REMOVE WARNING
os.environ["TOKENIZERS_PARALLELISM"] = "false"

nltk.download('stopwords')

df = pd.read_csv("datasets/sample.csv")
df.dropna(inplace=True)
df_en = pd.read_csv("datasets/en_df_nopunt.csv")
df_en.dropna(inplace=True)
print(len(df), "total documents, and", len(df_en), "are english")


random.seed(42)
sample = random.sample([x for x in df_en[['maintext', 'title', 'id']].to_numpy()], 100000)
documents = {str(idx): {'text': row[0][:512], 'title': row[1][:512], 'id': row[2]} for idx, row in enumerate(sample)}
print(len(documents), "total english documents")

# preprocessing only english documents
sp = WhiteSpacePreprocessing([a['title'] for a in documents.values()], stopwords_language='english')
preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()

tp = TopicModelDataPreparation("distiluse-base-multilingual-cased")

training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

num_topics = 5
ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=512, n_components=num_topics, num_epochs=500)
ctm.fit(training_dataset) # run the model

topics_predictions = ctm.get_thetas(training_dataset, n_samples=5) # get all the topic predictions

topic_list = ctm.get_topic_lists(10)

print(topic_list)
with open("dump/topics_layer_1.json", "w") as json_file:
    x = {i: t for i, t in enumerate(topic_list)}
    political_idx = 0
    for idx, v in enumerate(x.values()):
        if "brexit" in v:
            political_idx = idx
    json.dump(x, json_file)

print("political index is", political_idx)
print(x)


topic_mapper = {}
for k, v in documents.items():
    try:
        topic = int(np.argmax(topics_predictions[int(k)]))
        topic_mapper[v['id']] = topic
        documents[k]['topic'] = topic
    except:
        pass

with open('dump/topic_dump_l1.json', 'w') as json_file:
    json.dump(topic_mapper, json_file)

x = {idx: v for idx, v in enumerate(documents.values()) if v.get('topic', -1) == political_idx}

sp = WhiteSpacePreprocessing([a.get('text', '') for a in x.values()], stopwords_language='english')
preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()

tp = TopicModelDataPreparation("distiluse-base-multilingual-cased")

training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

num_topics = 8
ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=512, n_components=num_topics, num_epochs=50)
ctm.fit(training_dataset) # run the model

topics_predictions = ctm.get_thetas(training_dataset, n_samples=5) # get all the topic predictions

topic_list = ctm.get_topic_lists(10)

print(topic_list)
with open("dump/topics_layer_2.json", "w") as json_file:
    dump = {i: t for i, t in enumerate(topic_list)}
    json.dump(dump, json_file)


topic_mapper = {}
for k, v in x.items():
    try:
        topic = int(np.argmax(topics_predictions[int(k)]))
        topic_mapper[v.get('id', -1)] = topic
    except:
        pass

with open('dump/topic_dump_l2.json', 'w') as json_file:
    json.dump(topic_mapper, json_file)


