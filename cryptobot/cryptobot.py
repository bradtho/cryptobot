#!/usr/bin/env python3

import secret as secret
from auth import Auth as Auth
from account import Account as Account
from assets import Assets as Assets
from orders import Orders as Orders
import json
from tradingview_ta import *

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

                print(f'Updating Trailing Stoploss {assetId["code"]}')
                update = Orders(jwt).placeOrder(assetId["code"])

                stopLossTrigger = float(update["order"]["rate"]) * 0.9
                print(f'Setting Stop Loss: {stopLossTrigger}')
                Orders(jwt).updateOrder(assetId["code"], 6, stopLossTrigger)                
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
                print("No Buy Recommendations")
else:
    print("No Assets with Positions")
