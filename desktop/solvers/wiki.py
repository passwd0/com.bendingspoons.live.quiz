#! /usr/bin/env python3

import requests
import json
import wikipediaapi

wiki = wikipediaapi.Wikipedia('it')

f = open('../toignore', 'r')
raw = f.read()
f.close()
toIgnore = raw.split('\n')


def get_pages(query):
    params = {
            'action': 'query',
            'list': 'search',
            'srsearch': query,
            'format': 'json',
            }
    endpoint = 'http://it.wikipedia.org/w/api.php'
    results = json.loads(requests.get(endpoint,params).text)
    return results['query']['search']

# answers = list
def search(question, answers):
    print('[+] ' + question)
    results = {
            answers[0]:0,
            answers[1]:0,
            answers[2]:0,
            }
    for p in get_pages(question):
        print('    ', p['pageid'], p['title'])
        page = wiki.page(p['title'])
        if (page.exists()):
            content = page.text
        for a in answers:
            for w in a.split():
                if w not in toIgnore:
                    results[a] += content.lower().split().count(w.lower())
    return results
