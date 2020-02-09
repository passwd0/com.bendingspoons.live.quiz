#! /usr/bin/env python3

import json
from googleapiclient.discovery import build
import os.path
import re
from threading import Thread

DEBUG = False 
my_api_key = "***REMOVED***"
my_cse_id  = "***REMOVED***"
my_api_key = "***REMOVED***"
my_cse_id  = "***REMOVED***"
my_api_key = "***REMOVED***"
my_cse_id  = "***REMOVED***"


def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res

def google_search_or_cache(question, count, answer=None):
    if answer:
        q = f'{question} {answer}'
    else:
        q = question

    tmp = question[:55].replace('/','-')
    tmp = tmp.replace(' ','_')
    filename = f'dumps/{tmp}_{count}'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    else:
        data = google_search(q, my_api_key, my_cse_id)
        if DEBUG:
            with open(filename, 'w') as f:
                f.write(json.dumps(data))
    return data

def google_search_or_cache1(results, question, count, answers=None):
    if answers[count]:
        q = f'{question} {answers[count]}'
    else:
        q = question

    tmp = question[:55].replace('/','-')
    tmp = tmp.replace(' ','_')
    filename = f'dumps/{tmp}_{count+1}'
    if os.path.isfile(filename):
        with open(filename, 'r') as f:
            data = json.loads(f.read())
    else:
        data = google_search(q, my_api_key, my_cse_id)
        if DEBUG:
            with open(filename, 'w') as f:
                f.write(json.dumps(data))
    results[answers[count]]['tot'] = int(data['queries']['request'][0]['totalResults'])
    results = stat(data, answers, results)

def search(question, answers):
    results = {
            answers[0]:{'counterTot':0, 'counterPar':0, 'tot':0 },
            answers[1]:{'counterTot':0, 'counterPar':0, 'tot':0 },
            answers[2]:{'counterTot':0, 'counterPar':0, 'tot':0 }
    }

    # ricerca generale
    count=0
    data = google_search_or_cache(question, count)
    results = stat(data, answers, results)

    # ricerca specifica
    threads = []
    for s in results:
        t = Thread(target=google_search_or_cache1, args=(results, question, count, answers))
        count += 1
        t.start()
        threads.append(t)
        #data = google_search_or_cache(question, count, s)

    for i in threads:
        t.join()

    return results 

# conta parole
def stat(data, answers, results):
    for a in answers:           #per ogni risposta
        if 'items' in data.keys():
            for i in data['items']:
#                for ricercaField in ['title', 'snippet']:
#                    if ricercaField in i.keys():    # se ['title','ricerca'] esiste
                # parola completa
                if 'snippet' in i:
                    results[a]['counterTot'] += (i['snippet'].count(a.lower()))
                    # parola parziale presa in considerazione se CounterTot ha meno di 3 risultati
                    #if results[a]['counterTot'] < 3:
                    results[a]['counterPar'] += countWords(i['snippet'], a)
        # numero parole > 3 lettere
        nWordPiuDi3Lettere = 0
        for w in a.split():
            if w.isdigit() or len(w) > 3:
                nWordPiuDi3Lettere += 1
        if nWordPiuDi3Lettere > 0:  # inutile? quando non lo e'??
            results[a]['counterPar'] /= nWordPiuDi3Lettere
    return results

# conta il numero di wordsInAnswer in wordsInSnippet (insensitive case)
def countWords(wordsInSnippet, wordsInAnswer):
    wordsInSnippet = re.sub('[,:?;!\.\(\)]', '', wordsInSnippet)
    res = 0
    for k in wordsInAnswer.split():
        for i in wordsInSnippet.split():
            # se la parola(\w) ha meno di 3 lettere non viene contata
            if k.isalpha() and (len(k) < 3 or len(i) < 3):
                continue

            if k.isalpha() and k.lower()[:-1] == i.lower()[:-1]:
                res += 1
            if k.isdigit() and k == i:
                res += 1
    return res
