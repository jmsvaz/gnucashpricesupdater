import requests
import pandas

class FundosCVM:
    def __init__(self, fundoscvm_urlBase, fundoscvm_fileName, app_files_dir):

        self.__urlBase = fundoscvm_urlBase
        self.__fileName = fundoscvm_fileName
        self.__app_files_dir = app_files_dir
        self.__lastFileName = None  
        self.__df = None
        self.commodities = set()    

    def loadFile(self, date):
        period = date.replace('-','')[0:6]
        aFileName = self.__fileName.replace('{YYYYMM}',period)        
        fileName = self.__app_files_dir + aFileName
        url = self.__urlBase + aFileName

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

            df = pandas.read_csv(fileName, delimiter=';')
            if isinstance(df, pandas.DataFrame):
                self.__df =  df
                self.commodities = set(self.__df['CNPJ_FUNDO'].unique())
                print('  Download OK')
                self.__lastFileName = fileName
                return True
            else:
                return False

    def getQuotesByCnpjDate(self, cnpj, date):
        results = self.__df[(self.__df['CNPJ_FUNDO'] == cnpj) & (self.__df['DT_COMPTC'] == date)]
        if len(results) == 1:
            return results['VL_QUOTA'].iloc[0]
         