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

    def __newGuid(self):
        cur = self.__conn.cursor()
        #chech if guid exists
        guid = ""
        guidExists = True
        while(guidExists == True):
            guid = str(uuid.uuid4()).replace('-','')
            rowCount = len(cur.execute("select * from prices where guid = ?", (guid,)).fetchall())
            if rowCount == 0:
                guidExists = False
        return guid

    def __insertPrice(self, commodity_guid, currency_guid, date, value, denom):
        guid = self.__newGuid()
        cur = self.__conn.cursor()
        cur.execute("insert into prices (guid, commodity_guid, currency_guid, date, source, type, value_num, value_denom) values (?, ?, ?, ?, 'user:price', 'last', ?, ?)", (guid, commodity_guid, currency_guid, date + ' 05:00:00', value, denom,))
        self.__conn.commit()

    def __updatePrice(self, price_guid, value, denom):
        cur = self.__conn.cursor()
        cur.execute("update prices set value_num = ?, value_denom = ? where guid = ?", (value, denom, price_guid,))
        self.__conn.commit()

    def savePrices(self, priceList):
        conn = self.__conn
        updated = 0
        inserted = 0
        with conn:
            for p in priceList:
                tempPrice = self.__getPriceByCommodityDate(p.commodity_guid, p.date)

                #update
                if(len(tempPrice) == 1):
                    self.__updatePrice(tempPrice[0][0], p.value, p.denom)
                    updated += 1
                
                #insert
                if len(tempPrice) == 0:
                    self.__insertPrice(p.commodity_guid, p.currency_guid, p.date, p.value, p.denom)
                    inserted += 1
        if updated > 0:
            print('   Updated ' + str(updated) + ' prices')
        if inserted > 0:
            print('   Added ' + str(inserted) + ' new prices')

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