import pandas as pd
import numpy as np
import json

from sentence_transformers import SentenceTransformer
import umap
import hdbscan
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

df = pd.read_csv("sample.csv")
df.dropna(inplace=True)
print(len(df))
# COLUMNS = 'title', 'maintext', 'date_publish', 'language', 'source_domain', 'id'
content = [a[:512] for a in df.maintext]

# Multilingual knowledge distilled version of multilingual Universal Sentence Encoder. While v1 model supports 15 languages, 
# this version supports 50+ languages. However, performance on the 15 languages mentioned above are reported to be a bit lower.
model = SentenceTransformer('distiluse-base-multilingual-uncased-v2')
embeddings = model.encode(content, show_progress_bar=True)

umap_embeddings = umap.UMAP(n_neighbors=15, 
                            n_components=5, 
                            metric='cosine').fit_transform(embeddings)

cluster = hdbscan.HDBSCAN(min_cluster_size=15,
                          metric='euclidean',                      
                          cluster_selection_method='eom').fit(umap_embeddings)

# Prepare data
#umap_data = umap.UMAP(n_neighbors=15, n_components=2, min_dist=0.0, metric='cosine').fit_transform(embeddings)
#result = pd.DataFrame(umap_data, columns=['x', 'y'])
#result['labels'] = cluster.labels_

# Visualize clusters
#fig, ax = plt.subplots(figsize=(20, 10))
#outliers = result.loc[result.labels == -1, :]
#clustered = result.loc[result.labels != -1, :]
#plt.scatter(outliers.x, outliers.y, color='#BDBDBD', s=0.05)
#plt.scatter(clustered.x, clustered.y, c=clustered.labels, s=0.05, cmap='hsv_r')
#plt.colorbar()

docs_df = pd.DataFrame(content, columns=["Doc"])
docs_df['Topic'] = cluster.labels_
docs_df['Doc_ID'] = range(len(docs_df))
docs_per_topic = docs_df.groupby(['Topic'], as_index = False).agg({'Doc': ' '.join})

def c_tf_idf(documents, m, ngram_range=(1, 1)):
    count = CountVectorizer(ngram_range=ngram_range, stop_words="english").fit(documents)
    t = count.transform(documents).toarray()
    w = t.sum(axis=1)
    tf = np.divide(t.T, w)
    sum_t = t.sum(axis=0)
    idf = np.log(np.divide(m, sum_t)).reshape(-1, 1)
    tf_idf = np.multiply(tf, idf)

    return tf_idf, count
  
tf_idf, count = c_tf_idf(docs_per_topic.Doc.values, m=len(df))

def extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=20):
    words = count.get_feature_names()
    labels = list(docs_per_topic.Topic)
    tf_idf_transposed = tf_idf.T
    indices = tf_idf_transposed.argsort()[:, -n:]
    top_n_words = {label: [(words[j], tf_idf_transposed[i][j]) for j in indices[i]][::-1] for i, label in enumerate(labels)}
    return top_n_words

def extract_topic_sizes(df):
    topic_sizes = (df.groupby(['Topic'])
                     .Doc
                     .count()
                     .reset_index()
                     .rename({"Topic": "Topic", "Doc": "Size"}, axis='columns')
                     .sort_values("Size", ascending=False))
    return topic_sizes

top_n_words = extract_top_n_words_per_topic(tf_idf, count, docs_per_topic, n=50)
topic_sizes = extract_topic_sizes(docs_df)#; topic_sizes.head(10)

with open('topic_dump.json', 'w') as fp:
    json.dump(top_n_words, fp)
