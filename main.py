import pandas
import sqlite3
from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundsFileMng import FundsFileMng
from stockQuotes import StockQuotes
import settings


def numberOfDigits(value):
    return str(value)[::-1].find('.')

gc = GnuCashConn()
if not gc.loadFile():
    exit('GnuCash file not available!')

fundsFileMng = FundsFileMng()
if not fundsFileMng.loadFile(settings.date):
    exit('CVM file not available!')

stockQuotes = StockQuotes()
if not stockQuotes.loadFile(settings.date):
    exit('B3 file not available!')

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities()
newPriceList = []

for c in commodities:
    result = None
    if (c[1] in settings.CVM_Funds_commodities):
        result = fundsFileMng.getQuotesByCnpjDate(c[2], settings.date)

    if (c[1] in settings.B3_commodities):
        result = stockQuotes.getPriceByDate(c[2], settings.date)

    if result != None:
        newPrice = GnuCashPrice()
        newPrice.commodity_guid = c[0]
        newPrice.commodity_fullName = c[3]
        newPrice.currency_guid = brazilianCurrencyGuid
        newPrice.date = settings.date
        newPrice.denom = int(10 ** numberOfDigits(result))
        newPrice.value = int(result * newPrice.denom)
        newPriceList.append(newPrice)

if len(newPriceList) > 0:
    print('Updating commodities values from ' + settings.date + ':')
    gc.savePrices(newPriceList)