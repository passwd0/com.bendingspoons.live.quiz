#! /usr/bin/env python3

import requests

query = 'regina elisabetta'
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:70.0) Gecko/20100101 Firefox/70.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    #'Referer': 'https://ricerca.repubblica.it/ricerca/repubblica?query=&view=repubblica&ref=HRHS',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'TE': 'Trailers',
}

params = (
    ('query', 'regina elisabetta'),
    ('view', 'repubblica'),
)

r = requests.get('https://ricerca.repubblica.it/ricerca/repubblica', headers=headers, params=params)
print(r.text)

