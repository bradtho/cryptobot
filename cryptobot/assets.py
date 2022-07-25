#!/usr/bin/env python3

from urllib.error import HTTPError
from logs import Logs as Logs
import requests

class Assets:
    def __init__(self):
        self.apiurl = 'https://api.swyftx.com.au'
        self.headers = { 'Content-Type': 'application/json' }
        self.session = requests.Session()
        self.log = Logs.setupLogging("assets")        

    def getAssets(self, assetId):
        try:
            url = self.apiurl + f'/markets/info/basic/{assetId}/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            log = self.log
            r.raise_for_status()
            jsonResponse = r.json()
            return jsonResponse

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')
