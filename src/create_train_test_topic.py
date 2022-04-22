import pandas as pd 
import numpy as np

df = pd.read_csv("EUNewsArticles_w_topics", index_col=False)
df = df[df['topic'].notna()]
sizes = {k: len(df['topic'] == k) for k in np.unique(df.topic)}
min_size = min(sizes.values())

done = False
while not done:
    df_ = 
    if input("OK?") == 'y':
        done = True
        df_.to_csv("topic_modelling_traning_test.csv", index=False)