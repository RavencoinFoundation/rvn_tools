# Ravencoin Accountant
A python3 script to get deposits and withdrawals to/from addresses.  

The output goes to the console, and the date format is days from Jan 1, 1900 which is compatible with Google Sheets once formatted as a date.  

It uses the RavencoinPriceHistory.csv file to look up daily RVN price.  

Limitation: It works with single addresses like BalletWallet which don't use a different change address.  With a properly implemented change address, it is difficult to know which is the payment and which is the change.  

Usage: `python3 address_cpa.py > output.csv`
