# Ravencoin Accountant
A python3 script to get deposits and withdrawals to/from addresses.  

The output goes to the console, and the date format is days from Jan 1, 1900 which is compatible with Google Sheets once formatted as a date.  

It uses the RavencoinPriceHistory.csv file to look up daily RVN price.  

Limitation: It works with single addresses like BalletWallet which don't use a different change address.  With a properly implemented change address, it is difficult to know which is the payment and which is the change.  

Usage: `python3 address_cpa.py > output.csv`

### Sample Output

```
Date       txid                                                             address                            rvn_qty  rvn_price
12/21/2021 67e4dd9f85dfce43da4833db8d386eea7f40cbcf5bff1662fee36735913eea55 RVM93VRB9jn6FXps9mMu4iftxt7BpGexGM 226      0.0878
11/23/2021 b2fcd44ca469775707b9cd35eec17e8919d31c852c83e5ca2ff6a26a77e41e81 RVM93VRB9jn6FXps9mMu4iftxt7BpGexGM 250      0.1125
11/11/2021 ac4f018555a71d279ada5fbc02792b14386b34d4ecc3ceaf818b6464925b25f4 RVM93VRB9jn6FXps9mMu4iftxt7BpGexGM 300      0.1251
```