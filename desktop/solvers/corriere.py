#! /usr/bin/env python3


import requests


query = 'regina elisabetta'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': f'https://www.corriere.it/ricerca/index.shtml?q={query}',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
}

r = requests.get('https://www.corriere.it/search/COR/article/q=regina%2520elisabetta&lang=it&count=7&offset=0', headers=headers)

# torna un json :)
print(r.text)


