#!/usr/bin/env python3

from urllib.error import HTTPError
from logs import Logs as Logs
import requests

class Account:
    def __init__(self, jwt_token):
        self.apiurl = 'https://api.swyftx.com.au'
        self.auth = f'Bearer {jwt_token}'
        self.headers = { 'Content-Type': 'application/json', 'Authorization': self.auth }
        self.session = requests.Session()
        self.logs = Logs.setupLogging()

    def getProfile(self):
        try:
            url = self.apiurl + '/user/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            log = self.logs
            r.raise_for_status()
            jsonResponse = r.json()
            return jsonResponse

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')

    def getFavourites(self):
        try:
            url = self.apiurl + '/user/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            log = self.logs            
            r.raise_for_status()
            jsonResponse = r.json()["user"]["profile"]["userSettings"]["favouriteAssets"]
            return jsonResponse

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')            
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')

    def getBalances(self):
        try:
            url = self.apiurl + '/user/balance/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            log = self.logs            
            r.raise_for_status()
            jsonResponse = r.json()
            return jsonResponse

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')
