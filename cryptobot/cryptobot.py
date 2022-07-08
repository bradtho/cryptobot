#!/usr/bin/env python3

from urllib.error import HTTPError
import secret as secret
import requests
import json
from tradingview_ta import *

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
        except Exception as err:
            print(f'Other error occurred: {err}')

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
        except Exception as err:
            print(f'Other error occurred: {err}')

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
        except Exception as err:
            print(f'Other error occurred: {err}')

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
        except Exception as err:
            print(f'Other error occurred: {err}')

class Orders:
    def __init__(self, jwt_token):
        self.apiurl = 'https://api.swyftx.com.au'
        self.auth = f'Bearer {jwt_token}'
        self.useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        self.headers = { 'Content-Type': 'application/json', 'User-Agent': self.useragent, 'Authorization': self.auth }
        self.session = requests.Session()

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
    #         print(f'HTTP error occurred: {http_err}')
    #         print(f'{http_err.response.text}')
    #     except Exception as err:
    #         print(f'Other error occurred: {err}')

    def getOrder(self, orderUuid):
        try:
            url = self.apiurl + f'/orders/byId/{orderUuid}'
            h = self.headers
            r = self.session.get(url, headers=h)
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def placeOrder(self, asset):
        try:
            url = self.apiurl + '/orders/'
            h = self.headers
            d = f'''
            {{
                "primary": "AUD",
                "secondary": "{asset}",
                "quantity": "10",
                "assetQuantity": "AUD",
                "orderType": 1
            }}
            '''
            r = self.session.post(url, data=d, headers=h)
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')
            print(f'{err.response.text}')

    def updateOrder(self, asset, ordertype, trigger):
        try:
            url = self.apiurl + '/orders/'
            h = self.headers
            d = f'''
            {{
                "primary": "AUD",
                "secondary": "{asset}",
                "quantity": "10",
                "assetQuantity": "AUD",
                "orderType": {ordertype},
                "trigger": "{trigger}"
            }}
            '''
            r = self.session.post(url, data=d, headers=h)
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')

    def getHistory(self, assetId):
        try:
            url = self.apiurl + f'/portfolio/assetHistory/{assetId}/?page=1&limit=1&sortKey=date&sortDirection=DESC&type=BUY&status=COMPLETED'
            h = self.headers
            r = self.session.get(url, headers=h)
            r.raise_for_status()
            j = r.json()
            return j

        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
            print(f'{http_err.response.text}')
        except Exception as err:
            print(f'Other error occurred: {err}')

def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  print(percentage)

auth = Auth(secret.API_KEY)
jwt = (auth.getJWT())
account = Account(jwt)
assets = Assets()

# Move this into its own module - ideally run on a cronjob at midnight
# dust = set(())

# for assetId in account.getBalances():
#     availableBalance = float(assetId["availableBalance"])
#     if availableBalance < 1 and availableBalance != 0:
#         dust.add(assetId["assetId"])

# dustAssets = ', '.join([str(elem) for elem in dust])
# Orders(auth.getJWT()).dustAccount(dustAssets)        

openPosition = set(())
noPosition = set(())
favourite = set(())

for assetId in account.getFavourites():
    #Convert the type from key to int to clean up 's 
    assetId = int(assetId)
    favourite.add(assetId)

for assetId in account.getBalances():
    availableBalance = float(assetId["availableBalance"])
    if availableBalance != 0:
        openPosition.add(assetId["assetId"])
    else:
        noPosition.add(assetId["assetId"])

openPosition = set(openPosition).intersection(favourite)
noPosition = set(noPosition).intersection(favourite)

if openPosition:
    print ("Open Positions")
    for assetId in openPosition:
        for assetId in assets.getAssets(assetId):
            print (f'Details for: {assetId["name"]}, {assetId["code"]}')
            
            symbol = (assetId["code"] + "USDT")
            handler = TA_Handler(
                symbol=f"{symbol}",
                screener="crypto",
                exchange="binance",
                interval=Interval.INTERVAL_1_HOUR,
                timeout=60
            )
            rec = handler.get_analysis().summary
            print(rec)

            history = Orders(jwt).getHistory(assetId["id"])
            order = Orders(jwt).getOrder(history["items"][0]["uuid"])
            print(json.dumps(order, indent=2))

            if 'SELL' in rec.values() or 'STRONG_SELL' in rec.values():
                #implement a sell asset method
                print("sell")
            else:
                #implement a trailing stoploss method
                print("update order")
                print(order["orderUuid"])
                print(f'Order Buy Price AUD: {order["rate"]}')
                buyprice = (order["rate"])
                print(f'Current Sell Price AUD: {assetId["sell"]}')
                sellprice = (assetId["sell"])
                print("BUY:SELL Ratio")
                percentage(buyprice, sellprice)
else:
    print("No open positions")

if noPosition:
    print ("No Positions")
    for assetId in noPosition:
        for assetId in assets.getAssets(assetId):
            print (f'Details for: {assetId["name"]}, {assetId["code"]}')    

            symbol = (assetId["code"] + "USDT")
            handler = TA_Handler(
                symbol=f"{symbol}",
                screener="crypto",
                exchange="binance",
                interval=Interval.INTERVAL_1_HOUR,
                timeout=60
            )
            rec = handler.get_analysis().summary
            print(rec)

            if 'BUY' in rec.values() or 'STRONG_BUY' in rec.values():
                #implement an buy order method
                print(f'Market Buying {assetId["code"]}')
                buy = Orders(jwt).placeOrder(assetId["code"])

                if buy["order"]["status"] == 1:
                    stopLossTrigger = float(buy["order"]["rate"]) * 0.9
                    print(f'Setting Stop Loss: {stopLossTrigger}')
                    Orders(jwt).updateOrder(assetId["code"], 6, stopLossTrigger)     
                else:
                    print(f'Order Failed with Status: {buy["order"]["status"]}')
            else:
                #implement a trigger buy method
                print("Nothing Buy Recommendations")
else:
    print("No Assets with Positions")
