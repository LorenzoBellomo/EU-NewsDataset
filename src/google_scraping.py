'''
Per fare andare lo script con google è necessario creare un nuovo ambiente virtuale e scaricare:

- pip install google
- pip install --upgrade google-api-python-client

IMPORTANTE: non fare pip install googlesearch perchè è un'altra libreria non ufficiale e si creano collisioni
'''

from googlesearch import search   
import json
import pandas as pd

'''PARAMETER OF SEARCH
query: query string that we want to search for.
TLD: TLD stands for the top-level domain which means we want to search our results on google.com or google. in or some other domain.
lang: lang stands for language.
num: Number of results we want.
start: The first result to retrieve.
stop: The last result to retrieve. Use None to keep searching forever.
pause: Lapse to wait between HTTP requests. Lapse too short may cause Google to block your IP. Keeping significant lapses will make your program slow but it’s a safe and better option.
Return: Generator (iterator) that yields found URLs. If the stop parameter is None the iterator will loop forever.
'''


def make_google_query(query,domain):

    links = [] # lista in cui vengono memorizzati tutti i link (risultati) restituiti dalla chiamata a google search
    res = []
    for j in search(query, tld="co.in", num=3, stop=3, pause=2): # ci sta controllare solo i primi 3 risultati? facendo qualche test veloce mi sembrava che se il riultato fosse giusto lo individuava subito
        links.append(j) 
    
    # quello che volevo fare qua (ma probabilmente la stanchezza mi ha fregato) era controlla tra i link restituiti se ce ne uno che contiene il dominio che vogliamo e prendilo come risultato interropendo il check su gli altri
    # ha senso? poi nel controllo ho notato che cè un po di mismatch tra il nostro dominio e il loro (alcuni hanno www. altri no) quindi dovremmo fare un if che controlla sia che ce l'abbia o meno
    # insomma questa ultima parte non mi convince molto anche se i risultati sembrano essere buoni ma ne ho controllati una 20ina e
    # bisognerebbe controllare anche i nan
    for i in range(len(links)): 
        if domain.replace('www.','') in links[i]: 
            res = links[i]
            break
    return res

# dataset con gli articoli che sono in eu_data.csv ma non in EUNewsArticles.csv
to_find = pd.read_csv('/homenfs/l.bellomo1/BiasClassification/data/eudata_without_url.csv')
# a partire da questo dataset creo con un dizionario per fare scraping con chiave una tupla (titolo,id) e come valore il dominio dell'articolo
record_to_find = to_find.set_index(['title','id'])['source_domain'].to_dict()
results = dict() # nuovo dizionario in cui memorizzo in risultati con chiave titolo e valore (url,id)
for query,domain in record_to_find.items():

    print(query[0], query[1], domain) # stampo titolo,id,dominio
    res = make_google_query(query[0],domain) #chiamo lo scraper
    print(res)
    if res: # se il risultato è diverso da nan (quindi trova un url)
        results[query[1]] = (res.replace('https://',''),query[0]) # TODO: control this: memorizzo i risultati non so se ha senso togliere https e se vale per tutti (credo di si ma meglio controllare)
    else:
        results[query[1]] = None # altrimenti metto None a quell'entrata del dizionario
    # appendo ogni entrata del diz iterativamente ad un file json in modo da non perdere i risultati se si staccasse
    with open('/homenfs/l.bellomo1/BiasClassification/data/urls_all_data_eu.json', 'w') as outfile:
        json.dump(results, outfile)