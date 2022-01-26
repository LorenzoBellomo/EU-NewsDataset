#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
import json


from langdetect import detect
from matplotlib import pyplot as plt

from contextualized_topic_models.models.ctm import ZeroShotTM
from contextualized_topic_models.utils.data_preparation import TopicModelDataPreparation
from contextualized_topic_models.utils.preprocessing import WhiteSpacePreprocessing
import nltk

nltk.download('stopwords')


# In[4]:


df = pd.read_csv("datasets/sample.csv")
df.dropna(inplace=True)
len(df)
# COLUMNS = 'title', 'maintext', 'date_publish', 'language', 'source_domain', 'id'


# In[5]:


documents = [row[:512] for row in df[df['language'] == 'en'].maintext if detect(row[:512]) == 'en']
print(len(documents), "total english documents")


# In[6]:


sp = WhiteSpacePreprocessing(documents, stopwords_language='english')
preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()


# In[ ]:


tp = TopicModelDataPreparation("distiluse-base-multilingual-cased")

training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

num_topics = 5
ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=512, n_components=num_topics, num_epochs=20)
ctm.fit(training_dataset) # run the model


# In[ ]:


topic_list = ctm.get_topic_lists(10)
print(topic_list)

with open("dump/new_topics.json", "w") as json_file:
    json.dump(topic_list, json_file)


topics_predictions = ctm.get_thetas(training_dataset, n_samples=5) # get all the topic predictions


# In[11]:


for i in range(len(preprocessed_documents)):
    doc = preprocessed_documents[i]
    topic_number = np.argmax(topics_predictions[i])
    print(topic_number, " - ", doc)


# In[ ]:




