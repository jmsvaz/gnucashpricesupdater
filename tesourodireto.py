import requests
import pandas

class TesouroDireto:
    def __init__(self, td_url):
        self.__url = td_url
        self.__df = None
     #   self.commodities = set()    

    def loadFile(self, date):
        print('Requesting URL: ' + self.__url)
        if requests.head(self.__url).status_code == 200:
            self.__df = pandas.read_csv(self.__url, delimiter=';', decimal=',')
            self.__df['Data Vencimento'] = pandas.to_datetime(self.__df['Data Vencimento'], dayfirst=True)
            self.__df['Data Base'] = pandas.to_datetime(self.__df['Data Base'], dayfirst=True)
          #  self.commodities = set(self.__csvDf['CNPJ_FUNDO'].unique())
            print('  Download OK')
            return True
        else:
            return False

    def getQuotesByDate(self, bond, date):
        titulo,vencimento = bond.split(':') 
        vencimento = pandas.to_datetime(vencimento, format='%Y-%m-%d')
        date = pandas.to_datetime(date, format='%Y-%m-%d')
        df = self.__df
        df = df[(df['Tipo Titulo'] == titulo)]
        df = df[(df['Data Vencimento'] == vencimento)]

        if len(df) > 0:
            dfOnDate = df[(df['Data Base'] == date)]              
            if(len(dfOnDate) == 1):
                return dfOnDate['PU Venda Manha'].iloc[0]
        return None 