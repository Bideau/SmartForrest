#!/usr/bin/python
# -*- coding: utf-8 -*
import ConnectDB

class InsertDb(ConnectDB.ConnectDB):
    def __init__(self, path,name):
        ConnectDB.ConnectDB.__init__(self,path,name)
        self.connect()

    def insertIntoProbe(self, tabParameter):
        self.cursor.execute('INSERT INTO probe (p_name) VALUES (?)', tabParameter)

    def insertIntoValue(self, tabParameter):
        self.cursor.execute('INSERT INTO value ('
                               'v_date,'
                               'v_ozone,'
                               'v_temperature,'
                               'v_groundHumidity,'
                               'v_airHumidity,'
                               'v_probe) VALUES (?,?,?,?,?,?)', tabParameter)
