import pandas
import sqlite3
from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundsFileMng import FundsFileMng
from stockQuotes import StockQuotes
import settings


def numberOfDigits(value):
    return str(value)[::-1].find('.')

fundsFileMng = FundsFileMng()

if not fundsFileMng.loadFile(settings.date):
    exit('CVS file not available!')

gc = GnuCashConn()
stockQuotes = StockQuotes()

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities()
newPriceList = []

for c in commodities:
    newPrice = GnuCashPrice()
    newPrice.commodity_guid = c[0]
    newPrice.commodity_fullName = c[3]
    newPrice.currency_guid = brazilianCurrencyGuid
    newPrice.date = settings.date

    if (c[1] in settings.CVM_Funds_commodities):
        results = fundsFileMng.getQuotesByCnpjDate(c[2], settings.date)
        if len(results) == 1:
            price = results['VL_QUOTA'].iloc[0]
            newPrice.denom = int(10 ** numberOfDigits(price))
            newPrice.value = int(price * newPrice.denom)
            newPriceList.append(newPrice)
            #print('Add: ' + c[3])

    if (c[1] in settings.B3_commodities):
        result = stockQuotes.getPriceByDate(c[2], settings.date)
        if result != None:
            newPrice.denom = int(10 ** numberOfDigits(result))
            newPrice.value = int(result * newPrice.denom)
            newPriceList.append(newPrice)
            #print('Add: ' + c[3])

if len(newPriceList) > 0:
    gc.savePrices(newPriceList)