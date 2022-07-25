#!/usr/bin/env python3

import secret as secret
from auth import Auth as Auth
from account import Account as Account
from assets import Assets as Assets
from orders import Orders as Orders
from logs import Logs as Logs
import json
from tradingview_ta import *

def percentage(part, whole):
  percentage = 100 * float(part)/float(whole)
  return percentage

def main():
    auth = Auth(secret.API_KEY)
    jwt = (auth.getJWT())
    account = Account(jwt)
    assets = Assets()
    log = Logs.setupLogging("cryptbot")

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
        log.info("Open Positions")
        for assetId in openPosition:
            for assetId in assets.getAssets(assetId):
                log.info(f'Details for: {assetId["name"]}, {assetId["code"]}')
                
                symbol = (assetId["code"] + "USDT")
                handler = TA_Handler(
                    symbol=f"{symbol}",
                    screener="crypto",
                    exchange="binance",
                    interval=Interval.INTERVAL_1_HOUR,
                    timeout=60
                )
                rec = handler.get_analysis().summary
                log.info(rec)

                history = Orders(jwt).getHistory(assetId["id"])
                order = Orders(jwt).getOrder(history["items"][0]["uuid"])
                log.info(json.dumps(order, indent=2))

                if 'SELL' in rec.values() or 'STRONG_SELL' in rec.values():
                    #implement a sell asset method
                    log.info("sell")
                else:
                    #implement a trailing stoploss method
                    log.info(f'update order: {order["orderUuid"]}')
                    log.info(f'Order Buy Price AUD: {order["rate"]}')
                    buyprice = (order["rate"])
                    log.info(f'Current Sell Price AUD: {assetId["sell"]}')
                    sellprice = (assetId["sell"])
                    log.info("BUY:SELL Ratio")
                    percentage(buyprice, sellprice)

                    qtyToSell = round(float(order["amount"]), 6)

                    if percentage < 1:
                        log.info(f'Updating Trailing Stoploss for {assetId["code"]}')
                        stopLossTrigger = 1 / (float(order["rate"]) * 0.9)
                        log.info(f'Setting Stop Loss: {stopLossTrigger}')
                        #Orders(jwt).updateOrder(assetId["code"], qtyToSell, 6, stopLossTrigger)
                    else:
                        log.info(f'Leaving {order["orderUuid"]} intact')

    if noPosition:
        log.info ("No Open Positions")
        for assetId in noPosition:
            for assetId in assets.getAssets(assetId):
                log.info (f'Details for: {assetId["name"]}, {assetId["code"]}')    

                symbol = (assetId["code"] + "USDT")
                handler = TA_Handler(
                    symbol=f"{symbol}",
                    screener="crypto",
                    exchange="binance",
                    interval=Interval.INTERVAL_1_HOUR,
                    timeout=60
                )
                rec = handler.get_analysis().summary
                log.info(rec)

                if 'BUY' in rec.values() or 'STRONG_BUY' in rec.values():
                    #implement a buy order method
                    log.info(f'Market Buying {assetId["code"]}')
                    buy = Orders(jwt).placeOrder(assetId["code"])

                    if buy["order"]["status"] == 1:
                        qtyToSell = round(float(buy["order"]["amount"]), 6)
                        stopLossTrigger = 1 / (float(buy["order"]["rate"]) * 0.9)
                        log.info(f'Setting Stop Loss: {stopLossTrigger}')
                        Orders(jwt).updateOrder(assetId["code"], qtyToSell, 6, stopLossTrigger)     
                    else:
                        log.info(f'Order Failed with Status: {buy["order"]["status"]}')
                else:
                    #implement a trigger buy method
                    log.info("No Buy Recommendations")
