import sqlite3
import uuid
import os.path

class GnuCashConn:
    def __init__(self, gnucash_database_path):
        self.database_path = gnucash_database_path

    def loadFile(self):
        if os.path.exists(self.database_path):
            self.__conn = sqlite3.connect(self.database_path)
            return True
        else:
            return False    

    def generateGuid(self):
        return str(uuid.uuid4()).replace('-','')

    def createConn(self):
        return sqlite3.connect(self.database_path)
    
    def getCommodities(self):
        cur = self.__conn.cursor()
        cur.execute("select guid, namespace, mnemonic, fullname from commodities")
        return cur.fetchall()

    def getBrasilianCurrencyGuid(self):
        cur = self.__conn.cursor()
        cur.execute("select guid from commodities where namespace = 'CURRENCY' and mnemonic = 'BRL'")
        return cur.fetchone()[0]

    def __getPriceByCommodityDate(self, commodity_guid, date):
        cur = self.__conn.cursor()
        cur.execute("select guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom from prices where commodity_guid = ? and substr(date,1, 10) = ?", (commodity_guid, date,))
        return cur.fetchall()

    def __insertPrice(self, conn, commodity_guid, currency_guid, date, value, denom):
        cur = self.__conn.cursor()
        #chech if guid exists
        guid = ""
        guidExists = True
        while(guidExists == True):
            guid = self.generateGuid()
            rowCount = len(cur.execute("select * from prices where guid = ?", (guid,)).fetchall())
            if rowCount == 0:
                guidExists = False

        cur.execute("insert into prices (guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom) values (?, ?, ?, ?, 'user:price', 'last', ?, ?)", (guid, commodity_guid, currency_guid, date + ' 05:00:00', value, denom,))
        self.__conn.commit()

    def __updatePrice(self, conn, price_guid, value, denom):
        cur = self.__conn.cursor()
        cur.execute("update prices set value_num = ?, value_denom = ? where guid = ?", (value, denom, price_guid,))
        self.__conn.commit()

    def savePrices(self, priceList):
        conn = self.__conn
        with conn:
            for p in priceList:
                tempPrice = self.__getPriceByCommodityDate(p.commodity_guid, p.date)

                #update
                if(len(tempPrice) == 1):
                    self.__updatePrice(conn, tempPrice[0][0], p.value, p.denom)
                    print('  ' + p.commodity_fullName + ' - updated')
                
                #insert
                if len(tempPrice) == 0:
                    self.__insertPrice(conn, p.commodity_guid, p.currency_guid, p.date, p.value, p.denom)
                    print('  ' + p.commodity_fullName + ' - inserted')


class GnuCashPrice:
    def __init__(self, commodity_guid, commodity_fullName, currency_guid, date, denom, value):
        self.guid = ''
        self.commodity_guid = commodity_guid
        self.commodity_fullName = commodity_fullName
        self.currency_guid = currency_guid
        self.date = date
        self.source = 'user:price'
        self.type = 'last'
        self.denom = denom
        self.value = value