#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import numpy as np
from bertopic import BERTopic
import random
from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
import json

df = pd.read_csv(r"datasets/training_maintext_nopunt.csv")


#random.seed(42)
#random_keys = random.sample(list(df.id), 100000)
#documents = {row[1]: (row[0][:512], row[2], row[3]) for row in df[['maintext', 'id', 'year', 'political_leaning']].to_numpy() if row[1] in random_keys}
#with open('datasets/sample_topic_modelling.json', 'w') as json_file:
#    json.dump(documents, json_file)
with open('datasets/sample_topic_modelling.json', 'r') as json_file:
    documents = json.load(json_file)
docs = [a[0] for a in documents.values()]
print("loaded", len(docs), "documents")

#vectorizer_model = CountVectorizer(ngram_range=(1, 2), stop_words="english", min_df=10)
vectorizer_model = CountVectorizer(min_df=10)
sentence_model = SentenceTransformer("paraphrase-multilingual-mpnet-base-v2", device="cuda")
#topic_model = BERTopic(language="multilingual", embedding_model="paraphrase-multilingual-mpnet-base-v2", calculate_probabilities=False, verbose=True, low_memory=True, vectorizer_model=vectorizer_model)
topic_model = BERTopic(embedding_model=sentence_model, n_gram_range=(2,3), min_topic_size=100, nr_topics=50, calculate_probabilities=False, low_memory=True)
topics, probs = topic_model.fit_transform(docs)
#topics, probs = topic_model.reduce_topics(docs, topics, probs, nr_topics=50)

freq = topic_model.get_topic_info()

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

topics_over_time = topic_model.topics_over_time(docs, topics, [a[1] for a in documents.values()])

fig = topic_model.visualize_topics_over_time(topics_over_time, width=900, height=500)
fig.write_html("topic_dump/topics_over_time.html")

topics_per_class = topic_model.topics_per_class(docs, topics, classes=[a[2] for a in documents.values()])

fig = topic_model.visualize_topics_per_class(topics_per_class, width=900)
fig.write_html("topic_dump/topics_per_class.html")