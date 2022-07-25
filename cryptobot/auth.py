#!/usr/bin/env python3

from urllib.error import HTTPError
from logs import Logs as Logs
import requests

class Auth:
    def __init__(self, secret):
        self.apiurl = 'https://api.swyftx.com.au'
        self.headers = { 'Content-Type': 'application/json' }
        self.values = secret
        self.session = requests.Session()
        self.log = Logs.setupLogging("auth")

    def getJWT(self):
        try:
            url = self.apiurl + '/auth/refresh/'
            headers = self.headers
            values = self.values
            r = self.session.post(url, data=values, headers=headers)
            log = self.log
            jwt = r.json()['accessToken']
            return jwt

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')
