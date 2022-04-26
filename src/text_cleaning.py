from binhex import FInfo
from ctypes.wintypes import PUINT
from distutils.spawn import find_executable
import pandas as pd
import os
import json
from  builtins import any as b_any
from csv import writer
import matplotlib.pyplot as plt
import re
import string
import os
os.nice(10)



def clean_text(df, punt, to_clean):

    regex_pat = re.compile(r'\n', flags=re.IGNORECASE)
    df[to_clean] = df[to_clean].str.replace(regex_pat, " ")  # remove '\n' charac
    print('done')
    regex_pat2 = re.compile(r'[(http(s)?):\/\/(www\.)?a-zA-Z0-9@:%._\+~#=]{2,256}\.[a-z]{2,6}\b([-a-zA-Z0-9@:%_\+.~#?&//=]*)', flags=re.IGNORECASE) # remove http and www URL
    df[to_clean] = df[to_clean].str.replace(regex_pat2, " ")
    print('done')
    regex_pat3 = re.compile(r'\S*@[A-Za-z0-9_]*[.!?\\-]*[A-Za-z0-9_]*\S', flags=re.IGNORECASE) #remove mentions
    df[to_clean] = df[to_clean].str.replace(regex_pat3, " ")
    print('done')
    regex_pat4 = re.compile(r'#[A-Za-z0-9_]+', flags=re.IGNORECASE) # remove hastags
    df[to_clean] = df[to_clean].str.replace(regex_pat4, " ")
    print('done')
    regex_pat5 = re.compile(r'\([am][^ ]*| \(dpa[^ ]+ |\(dpa/es\)', flags=re.IGNORECASE) #remove 'dpa' or 'apa' characters
    df[to_clean] = df[to_clean].str.replace(regex_pat5, " ")
    print('done')
    regex_pat6 = re.compile(r'(?:(?:31(\/|-|\.)(?:0?[13578]|1[02]))\1|(?:(?:29|30)(\/|-|\.)(?:0?[13-9]|1[0-2])\2))(?:(?:1[6-9]|[2-9]\d)?\d{2})$|^(?:29(\/|-|\.)0?2\3(?:(?:(?:1[6-9]|[2-9]\d)?(?:0[48]|[2468][048]|[13579][26])|(?:(?:16|[2468][048]|[3579][26])00))))$|^(?:0?[1-9]|1\d|2[0-8])(\/|-|\.)(?:(?:0?[1-9])|(?:1[0-2]))\4(?:(?:1[6-9]|[2-9]\d)?\d{2})', flags=re.IGNORECASE) # remove date
    df[to_clean] = df[to_clean].str.replace(regex_pat6, " ")
    print('done')
    regex_pat7 = re.compile(r'\b(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]\b', flags=re.IGNORECASE) #remove timestamp
    df[to_clean] = df[to_clean].str.replace(regex_pat7, " ")
    print('done')
    regex_pat8 = re.compile(r'\S+\/(\w+)\/\S+', flags=re.IGNORECASE) #remove '/tag/'
    df[to_clean] = df[to_clean].str.replace(regex_pat8, " ")
    print('done')
    regex_pat9 = re.compile(r'[^.]*(FOTO|IMAGE|VIDEO|GETTY)[^.]*') #remove references to foto, video, images
    df[to_clean] = df[to_clean].str.replace(regex_pat9, " ")
    print('done')
    df[to_clean] = df[to_clean].str.replace('mehr dazu hier'," ")
    df[to_clean] = df[to_clean].str.replace('Ziare. com', " ")
    print('done')
    regex_pat10 = re.compile(r'<(.+?)>') #remove '<tag>'
    df[to_clean] = df[to_clean].str.replace(regex_pat10, " ")
    print('done')
    df[to_clean] = df[to_clean].str.replace('Get the biggest daily news stories by email Subscribe Thank you for subscribing We have more newsletters Show me See our privacy notice Could not subscribe, try again later Invalid Email', " ")
    regex_pat11 = re.compile(r'\[\.\.\.\]', flags=re.IGNORECASE) # remove '[...]'
    df[to_clean] = df[to_clean].str.replace(regex_pat11, " ")
    print('done')
    regex_pat12 = re.compile(r'\.\.\.$', flags=re.IGNORECASE) # remove '...' at the end of the article
    df[to_clean] = df[to_clean].str.replace(regex_pat12, " ")
    print('done')
    media = set(df['source_name'].to_list())
    media = list(media)
    media_upper = [elem.upper() for elem in media]
    
    print('done')
    df[to_clean] = df[to_clean].str.replace('|'.join(media),' ') # remove all media names
    df[to_clean] = df[to_clean].str.replace('|'.join(media_upper),' ')
    
    ## drop punctuation in the dataset in which it is required
    if punt == False:
        df[to_clean] = df[to_clean].str.replace('[^\w\s]','')
    
    # create a unique field composed by title and maintext for testing purposes
    df['all_text'] = df['title'] + ' ' + df['maintext']
    return df

'''
    all data textual fields cleaning
'''
'''
### training data maintext
print('\n')
print('----------------------------------')
print('all data maintext')
print('----------------------------------')
print('\n')
df = pd.read_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/training_with_topics.csv')
print(len(df))
punt = False
filtered_df = clean_text(df, punt, to_clean="maintext")
filtered_df.to_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/training_with_topics_cleaned.csv', index=False)
print(filtered_df.head(5))
print(len(filtered_df))
'''
### training data title
print('\n')
print('----------------------------------')
print('all data title')
print('----------------------------------')
print('\n')
df = pd.read_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/training_with_topics_cleaned.csv')
print(len(df))
punt = False
filtered_df = clean_text(df, punt, to_clean="title")
filtered_df.to_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/training_with_topics_cleaned.csv', index=False)
print(filtered_df.head(5))
print(len(filtered_df))
'''
### test data maintext
print('\n')
print('----------------------------------')
print('all data maintext')
print('----------------------------------')
print('\n')
df = pd.read_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/test_with_topics.csv')
print(len(df))
punt = False
filtered_df = clean_text(df, punt, to_clean="maintext")
filtered_df.to_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/test_with_topics_cleaned.csv', index=False)
print(filtered_df.head(5))
print(len(filtered_df))
'''
### test data title
print('\n')
print('----------------------------------')
print('all data title')
print('----------------------------------')
print('\n')
df = pd.read_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/test_with_topics_cleaned.csv')
print(len(df))
punt = False
filtered_df = clean_text(df, punt, to_clean="title")
filtered_df.to_csv('/homenfs/l.bellomo1/EU-NewsDataset/topic_modelling/data/test_with_topics_cleaned.csv', index=False)
print(filtered_df.head(5))
print(len(filtered_df))
