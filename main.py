from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundsFileMng import FundsFileMng
from stockQuotes import StockQuotes
import settings


def numberOfDigits(value):
    return str(value)[::-1].find('.')

gc = GnuCashConn(settings.gnucash_database_path)
if not gc.loadFile():
    exit('GnuCash file not available!')

fundsFileMng = FundsFileMng(settings.cvm_funds_url)
if not fundsFileMng.loadFile(settings.date):
    exit('CVM file not available!')

stockQuotes = StockQuotes(settings.b3_urlBase, settings.b3_fileNameBase, settings.app_files_dir)
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
        denom = int(10 ** numberOfDigits(result))
        value = int(result * denom)
        newPriceList.append(GnuCashPrice(c[0],c[3],brazilianCurrencyGuid,settings.date, denom, value))

if len(newPriceList) > 0:
    print('Updating commodities values from ' + settings.date + ':')
    gc.savePrices(newPriceList)