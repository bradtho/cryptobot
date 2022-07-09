#!/usr/bin/env python3

from urllib.error import HTTPError
import requests

class Auth:
    def __init__(self, secret):
        self.apiurl = 'https://api.swyftx.com.au'
        self.headers = { 'Content-Type': 'application/json' }
        self.values = secret
        self.session = requests.Session()

    def getJWT(self):
        try:
            url = self.apiurl + '/auth/refresh/'
            headers = self.headers
            values = self.values
            r = self.session.post(url, data=values, headers=headers)
            jwt = r.json()['accessToken']
            return jwt

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(f'{err.response.text}')
