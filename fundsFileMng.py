import requests
import pandas

class FundsFileMng:
    def __init__(self, cvm_funds_url):
        self.__url = cvm_funds_url
        self.__csvDf = None
        self.commodities = set()    

    def loadFile(self, date):
        period = date.replace('-','')[0:6]
        url = self.__url.replace('{YYYYMM}',period)
        print('Requesting URL: ' + url)
        if requests.head(url).status_code == 200:
            self.__csvDf = pandas.read_csv(url, delimiter=';')
            self.commodities = set(self.__csvDf['CNPJ_FUNDO'].unique())
            print('  Download OK')
            return True
        else:
            return False

    def getQuotesByCnpjDate(self, cnpj, date):
        results = self.__csvDf[(self.__csvDf['CNPJ_FUNDO'] == cnpj) & (self.__csvDf['DT_COMPTC'] == date)]
        if len(results) == 1:
            return results['VL_QUOTA'].iloc[0]
         