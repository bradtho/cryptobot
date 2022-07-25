#!/usr/bin/env python3

from urllib.error import HTTPError
from logs import Logs as Logs
import requests

class Orders:
    def __init__(self, jwt_token):
        self.apiurl = 'https://api.swyftx.com.au'
        self.auth = f'Bearer {jwt_token}'
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        self.headers = { 'Content-Type': 'application/json', 'User-Agent': self.useragent, 'Authorization': self.auth }
        self.session = requests.Session()
        self.log = Logs.setupLogging("orders")

    # Move this into its own package  - ideally run on a cronjob at midnight
    # def dustAccount(self, dustPosition):
    #     try:
    #         u = self.apiurl + '/user/balance/dust/'
    #         h = self.headers
    #         d = f'''
    #         {{
    #             "selected": [
    #             {dustPosition}
    #             ],
    #             "primary": 1
    #         }}
    #         '''
    #         r = self.session.post(u, data=d, headers=h)
    #         r.raise_for_status()
    #         j = r.json()      
    #         return j

    #     except requests.exceptions.HTTPError as http_err:
    #         log.error(f'HTTP error occurred: {http_err}')
    #         log.error(f'{http_err.response.text}')
    #     except Exception as err:
    #         log.exception(f'Other error occurred: {err}')
    #         log.exception(f'{err.response.text}')

    def getOrder(self, orderUuid):
        try:
            url = self.apiurl + f'/orders/byId/{orderUuid}'
            h = self.headers
            r = self.session.get(url, headers=h)
            log = self.log
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')

    def placeOrder(self, asset):
        try:
            url = self.apiurl + '/orders/'
            h = self.headers
            d = f'''
            {{
                "primary": "AUD",
                "secondary": "{asset}",
                "quantity": "5",
                "assetQuantity": "AUD",
                "orderType": 1
            }}
            '''
            r = self.session.post(url, data=d, headers=h)
            log = self.log
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')

    def updateOrder(self, asset, quantity, ordertype, trigger):
        try:
            url = self.apiurl + '/orders/'
            h = self.headers
            d = f'''
            {{
                "primary": "AUD",
                "secondary": "{asset}",
                "quantity": "{quantity}",
                "assetQuantity": "AUD",
                "orderType": {ordertype},
                "trigger": "{trigger}"
            }}
            '''
            r = self.session.post(url, data=d, headers=h)
            log = self.log
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')

    def getHistory(self, assetId):
        try:
            url = self.apiurl + f'/portfolio/assetHistory/{assetId}/?page=1&limit=1&sortKey=date&sortDirection=DESC&type=BUY&status=COMPLETED'
            h = self.headers
            r = self.session.get(url, headers=h)
            log = self.log
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            log.error(f'HTTP error occurred: {http_err}')
            log.error(f'{http_err.response.text}')
        except Exception as err:
            log.exception(f'Other error occurred: {err}')
            log.exception(f'{err.response.text}')
