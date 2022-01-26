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

nltk.download('stopwords')



df = pd.read_csv(r"datasets/training_maintext_nopunt.csv")
len(df)
df.dropna(inplace=True)
len(df)
print(df.head())
# COLUMNS = 'title', 'maintext', 'date_publish', 'language', 'source_domain', 'id'


documents_en = {row[1]: row[0][:512] for row in df[df['language'] == 'en'][['maintext', 'id']].to_numpy()} #if detect(row[0][:512]) == 'en'}
print(len(documents_en), "total english documents")
documents_non_en = {row[1]: row[0][:512] for row in list(df[['maintext', 'id']].to_numpy()) if row[1] not in documents_en.keys()}
print(len(documents_non_en), "total non english documents")
print((len(documents_en) + len(documents_non_en)), "is the sum")

sp = WhiteSpacePreprocessing(list(documents_en.values()), stopwords_language='english')
preprocessed_documents, unpreprocessed_corpus, vocab = sp.preprocess()


tp = TopicModelDataPreparation("distiluse-base-multilingual-cased")

training_dataset = tp.fit(text_for_contextual=unpreprocessed_corpus, text_for_bow=preprocessed_documents)

num_topics = 5
ctm = ZeroShotTM(bow_size=len(tp.vocab), contextual_size=512, n_components=num_topics, num_epochs=20)
ctm.fit(training_dataset) # run the model


topic_list = ctm.get_topic_lists(10)
print(topic_list)

with open("dump/new_topics.json", "w") as json_file:
    json.dump(topic_list, json_file)


topics_predictions = ctm.get_thetas(training_dataset, n_samples=5) # get all the topic predictions

topic_mapper = {}
for i, k in enumerate(list(documents_en.keys())):
    topic_number = np.argmax(topics_predictions[i])
    topic_mapper = {k: topic_number} 


# NON EN PART
testing_dataset = tp.transform(list(documents_non_en.values())) # create dataset for the testset
italian_topics_predictions = ctm.get_thetas(testing_dataset, n_samples=5) # get all the topic predictions

for i, k in enumerate(list(documents_non_en.keys())):
    topic_number = np.argmax(italian_topics_predictions[i])
    topic_mapper = {k: topic_number} 

with open("dump/new_topic_mapper.json", "w") as json_file:
    json.dump(topic_mapper, json_file)