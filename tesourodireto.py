import requests
import pandas

class TesouroDireto:
    def __init__(self, tesourodireto_urlBase, tesourodireto_fileName, app_files_dir):
        self.__urlBase = tesourodireto_urlBase
        self.__fileName = tesourodireto_fileName
        self.__app_files_dir = app_files_dir
        self.__lastFileName = None        
        self.__df = None
        self.commodities = set()    

    def loadFile(self, date):       
        fileName = self.__app_files_dir + self.__fileName
        url = self.__urlBase + self.__fileName

        if self.__lastFileName == fileName:
            print('Using last downloaded file: ' + fileName) 
            return True  
        else:  
            print('Requesting URL: ' + url)
            if requests.head(url).status_code == 200:
                request = requests.get(url)
                with open(fileName, 'wb') as f:
                    f.write(request.content)

            else:
                return False

            df = pandas.read_csv(fileName, delimiter=';', decimal=',')
            if isinstance(df, pandas.DataFrame):
                self.__df =  df
                self.__df['Data Vencimento'] = pandas.to_datetime(self.__df['Data Vencimento'], dayfirst=True)
                self.__df['Data Base'] = pandas.to_datetime(self.__df['Data Base'], dayfirst=True)
            #  self.commodities = set(self.__csvDf['CNPJ_FUNDO'].unique())
                print('  Download OK')
                self.__lastFileName = fileName
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