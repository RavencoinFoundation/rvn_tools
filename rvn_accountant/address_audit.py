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
rvnsum = 0.0
master_balance = 0.0

def audit_address(addr):
	global rvnsum
	global master_balance
	rvnsum = 0
	tot = 0
	print("Auditing: " + addr)
	balance = get_balance(addr);
	txids = get_txids(addr)
	for tx in reversed(txids):
		#print (tx)
		tot = get_rvn_qty_deposit(addr, tx)

	master_balance += tot
	print_summary(balance, tot)


def print_summary(balance, total):
	print(format(balance, '.8f') + ' = ' + format(total, '.8f'))
	#print(bal)
	#print(total)
	if (balance == total):
		print("Audit passed")
	else:
		print("Audit failed")
	print('')
	print('')


def print_master_balance():
	global master_balance
	print('')
	print("Balance of all addresses: " + format(master_balance,'.8f'))

def get_balance(addr):
	url = api_root+'addr'+'/'+addr
	balinfo = get_json(url)
	print("Balance: " + str(balinfo['balance']))
	return(balinfo['balance'])

# def payment_amount(txinfo, addr):
# 	#print(vins)
# 	for vin in txinfo['vin']:
# 		if vin.get('addr') == addr:
# 			return vin['value'];
# 	return 0.0


def payment_amount(txinfo, addr):
	totvalue = 0.0
	#print(vins)
	for vin in txinfo['vin']:
		if vin.get('addr') == addr:
			totvalue += vin['value']
	return float(format(totvalue, '.8f'))



def get_rvn_qty_deposit(addr, tx):
	global rvnsum
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
					price = look_up_price(txinfo['blocktime'])
					rvn = float(vout['value']) - valueIn
					rvnsum += rvn
					print(str(epoch_to_days_since_1900(txinfo['blocktime'])) + ',' + tx + ',' + vout['scriptPubKey']['addresses'][0] + ',' + str(rvn) + ',' + price + " Tot: " + format(rvnsum, '.8f'))
	except:
		print('Problem with tx: ' + tx)
		print(e.message)

	return float(format(rvnsum, '.8f'))


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


audit_address("RVM93VRB9jn6FXps9mMu4iftxt7BpGexGM")
audit_address("RXAnmAHpGxsN8NnEcmg3DGZw1oS2WrNWiN")
audit_address("RCiwkUmjomjLimfg7WetZKWM8zsuX9ATh7")
audit_address("RDLLeDZf4wgaEn16CfeEhKDvuVEz5Ne8ch")
audit_address("RQgaUTY2TXqngsvPJW3EjqnPVxH5yahqeB")
audit_address("RQYtTcMaUX9XZER8cGz2dLYPGycNfFpaSW")
audit_address("RANFH4yGXr766LWoCSv2PYXH5NuyMSNG2S")
audit_address("RJzkp2xcXkEQYXYfZzdBTrvCNxy2GKqjLn")
audit_address("RBzm8wmbEcdFxAWAZ2stkxSN615uDgvqCd")
audit_address("RBP8BcvCm25oMp3WQd3E2RFrE1kaYvLgub")
audit_address("RR3wMq5pjmFf8gd2iJLb3qEtjR3xjAEaR8")

print_master_balance()



 






