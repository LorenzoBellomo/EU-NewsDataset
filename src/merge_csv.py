import pandas as pd 
import numpy as np

df1 = pd.read_csv("EUNewsArticles.csv", index_col=False)
df2 = pd.read_csv("BiasClassification/data/eudata_without_url.csv", index_col=False)
df2['url'] = np.nan
df = pd.concat([df1, df2], ignore_index=True)
df.to_csv("EUAllData.csv")