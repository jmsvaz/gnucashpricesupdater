from gnucashConn import GnuCashConn
from gnucashConn import GnuCashPrice
from fundosCVM import FundosCVM
from B3 import B3
from tesourodireto import TesouroDireto
import settings

print('GnuCash Price Updater')

def numberOfDigits(value):
    return str(value)[::-1].find('.')

gc = GnuCashConn(settings.gnuCashFile)
if not gc.loadFile():
    exit(' # GnuCash file not available!')

fundosCVM = FundosCVM(settings.fundoscvm_urlBase, settings.fundoscvm_fileName, settings.app_files_dir)

b3 = B3(settings.b3_urlBase, settings.b3_fileName, settings.app_files_dir)

tesouroDireto = TesouroDireto(settings.tesourodireto_urlBase, settings.tesourodireto_fileName, settings.app_files_dir)

brazilianCurrencyGuid = gc.getBrasilianCurrencyGuid()
commodities = gc.getCommodities()
newPriceList = []

for date in settings.dates:
    print('Searching prices for ' + date + ':')

    if not fundosCVM.loadFile(date):
        print(' # CVM file not available!')
    else:
        for c in commodities:
            result = None
            if (c[1] in settings.fundoscvm_namespace):
                result = fundosCVM.getQuotesByCnpjDate(c[2], date)
            if result != None:
                denom = int(10 ** numberOfDigits(result))
                value = int(result * denom)
                print('  Found price for ' + c[3])
                newPriceList.append(GnuCashPrice(c[0],c[3],brazilianCurrencyGuid,date, denom, value))
                
    if not b3.loadFile(date):
            print(' # B3 file not available!')
    else:
        for c in commodities:
            result = None
            if (c[1] in settings.b3_namespace):
                result = b3.getPriceByDate(c[2], date)
            if result != None:
                denom = int(10 ** numberOfDigits(result))
                value = int(result * denom)
                print('  Found price for ' + c[3])
                newPriceList.append(GnuCashPrice(c[0],c[3],brazilianCurrencyGuid,date, denom, value))

    if not tesouroDireto.loadFile(date):
        print(' # TD file not available!')
    else:
        for c in commodities:
            result = None
            if (c[1] in settings.tesourodireto_namespace):
                result = tesouroDireto.getQuotesByDate(c[2], date)
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