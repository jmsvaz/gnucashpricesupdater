import requests
import pandas
import os.path
from time import sleep
from zipfile import ZipFile

class StockQuotes:
    def __init__(self, b3_urlBase, b3_fileNameBase, app_files_dir):
        self.__urlBase = b3_urlBase
        self.__fileNameBase = b3_fileNameBase
        self.__app_files_dir = app_files_dir
        self.__df = None

    def loadFile(self, date):
        period = date.replace('-','')[4:6] + date.replace('-','')[0:4]
        aFileName = self.__fileNameBase.replace('{MMYYYY}', period)        
        fileName = self.__app_files_dir + aFileName
        url = self.__urlBase + aFileName
        
        print('Requesting URL: ' + url)
        header = requests.head(url)

        if header.status_code == 200 and header.headers['content-type'] == 'application/x-zip-compressed':
            request = requests.get(url)
            with open(fileName, 'wb') as f:
                f.write(request.content)

        else:
            return False


        with ZipFile(fileName, 'r') as zipObj:
            zipObj.extractall(self.__app_files_dir)

        df = pandas.read_fwf(fileName.replace('ZIP','TXT'), names=['type', 'date', 'stock', 'price'], header=None, colspecs=[(0,2), (2,10), (12,24), (109,121)])
        df['price'] = df['price'].map(lambda price: price / 100)
        if isinstance(df, pandas.DataFrame):
            self.__df =  df
            print('  Download OK')
            return True
        else:
            return False          

    def getPriceByDate(self, stock, date):
        """Returns a value or None
        stock -- code of ticker
        function -- StockQuotes.StockQuotesFunction
        date -- string formated as YYYY-MM-DD
        """

        df = self.__df
        df = df[(df['stock'] == stock)]

        if isinstance(df, pandas.DataFrame):
            if len(df) > 0:
                dfOnDate = df[(df['date'] == date.replace('-',''))]
                
                if(len(dfOnDate) == 1):
                    return dfOnDate['price'].iloc[0]
        
        return None