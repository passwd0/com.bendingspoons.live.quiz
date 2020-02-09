#! /usr/bin/env python3


import requests

query = 'regina elisabetta'
params = {
        's':query,
        }
endpoint = 'https://ilpost.it'
r = requests.get(endpoint, params)
print(r.text)


