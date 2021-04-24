from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundsFileMng import FundsFileMng
from stockQuotes import StockQuotes
import settings

print('GnuCash Price Updater')

def numberOfDigits(value):
    return str(value)[::-1].find('.')

gc = GnuCashConn(settings.gnucash_database_path)
if not gc.loadFile():
    exit(' # GnuCash file not available!')

fundsFileMng = FundsFileMng(settings.cvm_funds_url)

stockQuotes = StockQuotes(settings.b3_urlBase, settings.b3_fileNameBase, settings.app_files_dir)

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities()
newPriceList = []

for date in settings.dates:
    print('Searching prices for ' + date + ':')

    if not fundsFileMng.loadFile(date):
        print(' # CVM file not available!')
    else:
        for c in commodities:
            result = None
            if (c[1] in settings.CVM_Funds_commodities):
                result = fundsFileMng.getQuotesByCnpjDate(c[2], date)
            if result != None:
                denom = int(10 ** numberOfDigits(result))
                value = int(result * denom)
                print('  Found price for ' + c[3])
                newPriceList.append(GnuCashPrice(c[0],c[3],brazilianCurrencyGuid,date, denom, value))
                
    if not stockQuotes.loadFile(date):
            print(' # B3 file not available!')
    else:
        for c in commodities:
            result = None
            if (c[1] in settings.B3_commodities):
                result = stockQuotes.getPriceByDate(c[2], date)
            if result != None:
                denom = int(10 ** numberOfDigits(result))
                value = int(result * denom)
                print('  Found price for ' + c[3])
                newPriceList.append(GnuCashPrice(c[0],c[3],brazilianCurrencyGuid,date, denom, value))

if len(newPriceList) > 0:
    print('Updating GnuCash:')
    gc.savePrices(newPriceList)
else:
    print('No prices found!')