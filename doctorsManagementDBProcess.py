#!/bin/python

import MySQLdb as mySql
from time import sleep
import datetime 

class dbManagement():
    
    def __init__(self):
        self.dbConn = mySql.connect("localhost", "root")
        self.dbCursor = self.dbConn.cursor()
        self.dbCursor.execute("use DoctorsManagement")

    def tableInsertion(self, tableName, values):
        query = "insert into "+ tableName +" values" + str(values)
        print "query = ", query
        self.dbCursor.execute(query)
        self.dbConn.commit()

    def tableSelect(self, tableName, condition=None, wantedData=None):
        if condition and not wantedData:
            query = "select * from "+ tableName + " where "+ condition
        elif condition == "last":
            if wantedData:
                query = "select max("+wantedData+") from "+ tableName 
        else:

            query = "select * from "+ tableName
        self.dbCursor.execute(query)
        data = self.dbCursor.fetchall()
        return data

    def tableUpdation(self, tableName, values):
        query = "update "+ tableName + " set "+ values
        print query
        self.dbCursor.execute(query)
        self.dbConn.commit()

    
    def tableDeletion(self, tableName, condition):
        query = "delete from "+ tableName +" where "+ condition
        self.dbCursor.execute(query)
        self.dbConn.commit()

                
    
'''       
test = dbManagement()
print type(test.tableSelect("Patients", "Token=1")[0][1])
'''



