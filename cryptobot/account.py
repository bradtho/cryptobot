#!/usr/bin/env python3

from urllib.error import HTTPError
import requests

class Account:
    def __init__(self, jwt_token):
        self.apiurl = 'https://api.swyftx.com.au'
        self.auth = f'Bearer {jwt_token}'
        self.headers = { 'Content-Type': 'application/json', 'Authorization': self.auth }
        self.session = requests.Session()

    def getProfile(self):
        try:
            url = self.apiurl + '/user/'
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

    def getFavourites(self):
        try:
            url = self.apiurl + '/user/'
            headers = self.headers
            r = self.session.get(url, headers=headers)
            r.raise_for_status()
            jsonResponse = r.json()["user"]["profile"]["userSettings"]["favouriteAssets"]
            return jsonResponse

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(f'{err.response.text}')

    def getBalances(self):
        try:
            url = self.apiurl + '/user/balance/'
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
