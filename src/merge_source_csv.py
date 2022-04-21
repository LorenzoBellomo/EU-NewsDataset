import pandas as pd 
import glob 
import os

files = os.path.join("final_dataset/", "*.csv")
files = glob.glob(files)
print(files)
df = pd.concat(map(pd.read_csv, files), ignore_index=True)
df.to_csv("EUNewsArticles.csv", index=False)