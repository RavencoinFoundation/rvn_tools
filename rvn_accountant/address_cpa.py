#!/usr/bin/env python3
# Script to get deposits and withdrawals from a specific Ravencoin address
# Reads from APIs to get transactions
# Gets the transaction information 
# Gets the price (at the time)
# Outputs to console - CSV compatible with Google Sheets

import os
import subprocess
import json
import logging
from urllib.request import urlopen
import csv
from datetime import timezone
import datetime

RavencoinPriceHistory = dict()


api_root = 'https://api.ravencoin.org/api/'


def scan_address(addr, start_date_epoch, end_date_epoch):
	txids = get_txids(addr)
	for tx in reversed(txids):
		#print (tx)
		qty = get_rvn_qty_deposit(addr, tx, start_date_epoch, end_date_epoch)


def payment_amount(txinfo, addr):
	totvalue = 0.0
	#print(vins)
	for vin in txinfo['vin']:
		if vin.get('addr') == addr:
			totvalue += vin['value']
	return float(format(totvalue, '.8f'))



def get_rvn_qty_deposit(addr, tx, start_date_epoch, end_date_epoch):
	url = api_root+'tx'+'/'+tx
	#print(url)   #debug
	txinfo = get_json(url)

	#If we are paying, then the payment amount comes from this address, and the change goes back to vout (will show as negative)
	valueIn = payment_amount(txinfo, addr)

	try:
		for vout in txinfo['vout']:
			if float(vout['value']) > 0:
				if vout['scriptPubKey']['addresses'][0] == addr:
					#print(txinfo)
					if ( (txinfo['blocktime'] >= start_date_epoch) and (txinfo['blocktime'] < end_date_epoch) ):
						price = look_up_price(txinfo['blocktime'])
						print(str(epoch_to_days_since_1900(txinfo['blocktime'])) + ',' + tx + ',' + vout['scriptPubKey']['addresses'][0] + ',' + str(float(vout['value']) - valueIn) + ',' + price)
	except:
		print('Problem with tx: ' + tx)
		print(e.message)

	return 0


def epoch_to_days_since_1900(epoch):
	xtra_days = 25567  #80 years of days.  Google uses days since Jan 1, 1900 and epoch uses 1970
	return(epoch / 86400 + xtra_days) 

def look_up_price(epoch_time):
	secs_per_day = 24*60*60
	day_epoch_time = int(epoch_time / secs_per_day) * secs_per_day
	#print("Looking up " + str(day_epoch_time))     #debug
	return RavencoinPriceHistory[day_epoch_time]



def get_json(url):
	urldata = urlopen(url).read()
	json_data = json.loads(urldata)
	return(json_data)

def get_txids(addr):
	url = api_root+'addr'+'/'+addr
	#print(url)  #debug
	raw_json = get_json(url)
	tx_data = raw_json['transactions']
	return(tx_data)

def convert_date_string_to_timestamp(date_string):
	dt = datetime.datetime.strptime(date_string,"%b %d, %Y") 
	ts = int(dt.replace(tzinfo=timezone.utc).timestamp()) 
	#ts = datetime.datetime.ts(time)
	return(ts) 

def load_price_data(csv_file):
	with open(csv_file, "r") as csvfile:
	    #print(rpc_call('getbestblockhash'))
	    reader = csv.DictReader(csvfile)
	    for daily_price in reader:
	    	#RavencoinPriceHistory[] = daily_price.get('Open')
	    	RavencoinPriceHistory[convert_date_string_to_timestamp(daily_price.get('Date'))] = daily_price.get('Open')
	    	#DEBUG for price data import
	    	#print(daily_price.get('Date'))
	    	#print(convert_date_string_to_timestamp(daily_price.get('Date')))
	    	#print(daily_price.get('Open'))



#print('Loading Ravencoin Price History')
load_price_data('RavencoinPriceHistory.csv')
#print(RavencoinPriceHistory)
try:
	test_price = RavencoinPriceHistory[1660176000]
except:
	print("Ravencoin Price import failed - Look for updated RavencoinPriceHistory.csv")
	print(e.message)

start_date = 1609484400    #Jan 01 2021 00:00:00 UTC
end_date   = 1641020400    #Jan 01 2022 00:00:00 UTC

#Before start
#start_date = 1514815200    #Jan 01 2018 00:00:00 UTC
#end_date   = 1609484400    #Jan 01 2021 00:00:00 UTC
#end_date   = 1641020400    #Jan 01 2022 00:00:00 UTC
#end_date   = 1672581600    #Jan 01 2023 00:00:00 UTC

print("Date,txid,address,rvn_qty,rvn_price")
scan_address("RVM93VRB9jn6FXps9mMu4iftxt7BpGexGM", start_date, end_date)
scan_address("RXAnmAHpGxsN8NnEcmg3DGZw1oS2WrNWiN", start_date, end_date)
scan_address("RCiwkUmjomjLimfg7WetZKWM8zsuX9ATh7", start_date, end_date)
scan_address("RDLLeDZf4wgaEn16CfeEhKDvuVEz5Ne8ch", start_date, end_date)
scan_address("RQgaUTY2TXqngsvPJW3EjqnPVxH5yahqeB", start_date, end_date)
scan_address("RQYtTcMaUX9XZER8cGz2dLYPGycNfFpaSW", start_date, end_date)
scan_address("RANFH4yGXr766LWoCSv2PYXH5NuyMSNG2S", start_date, end_date)
scan_address("RJzkp2xcXkEQYXYfZzdBTrvCNxy2GKqjLn", start_date, end_date)
scan_address("RBzm8wmbEcdFxAWAZ2stkxSN615uDgvqCd", start_date, end_date)
scan_address("RBP8BcvCm25oMp3WQd3E2RFrE1kaYvLgub", start_date, end_date)
scan_address("RR3wMq5pjmFf8gd2iJLb3qEtjR3xjAEaR8", start_date, end_date)







