#!/usr/bin/env python3

from urllib.error import HTTPError
import requests

class Assets:
    def __init__(self):
        self.apiurl = 'https://api.swyftx.com.au'
        self.headers = { 'Content-Type': 'application/json' }
        self.session = requests.Session()

    def getAssets(self, assetId):
        try:
            url = self.apiurl + f'/markets/info/basic/{assetId}/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            jsonResponse = r.json()
            return jsonResponse

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(f'{err.response.text}')
