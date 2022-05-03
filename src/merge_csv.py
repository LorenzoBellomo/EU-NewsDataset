import pandas as pd 
import numpy as np

df1 = pd.read_csv("EUNewsArticles.csv", index_col=False)
df2 = pd.read_csv("BiasClassification/data/eudata_without_url.csv", index_col=False)
df2['url'] = np.nan
df2.drop(columns=['date'], inplace=True)
df1.drop(columns=['topic', 'topic2'], inplace=True)
df2=df2[df1.columns]
df = pd.concat([df1, df2], ignore_index=True, sort=False, axis = 0)
df.to_csv("EUAllData.csv")