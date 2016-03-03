#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time

import dataBase.sqlite3.QueryDb
from dataBase.sqlite3 import CreateDB, CreateDB2, InsertDb

path = "../ressources/"
name = "db.db"
path2 = "../ressources/"
name2 = "db2.db"
rangeP = 10
rangeV = 144

#creation de la db
mydb = CreateDB.CreateDB(path, name)
mydb.create()
mydb.close

#creation de la db2
mydb2 = CreateDB2.CreateDB2(path2, name2)
mydb2.create()
mydb2.close

# insertion data
myinsertdb = InsertDb.InsertDb(path, name)

for i in range(1,rangeP):
    _name = "probe " + str(i)
    _latitude = random.uniform(-90,90)
    _longitude = random.uniform(-180,180)
    parameter = [_name,_longitude,_latitude]
    myinsertdb.insertIntoProbe(parameter)

#insert dans value
for i in range(1,rangeP):
    for j in range(0,rangeV):
        _date = time.time()
        _ozone = random.uniform(40,70)
        _temperature = random.uniform(20,30)
        _humidity = random.uniform(10,60)
        _hygrometry = random.uniform(10,60)
        _waterTemperature = random.uniform(5,20)
        _waterLevel = random.uniform(0,20)
        _probe = i
        parameter = [_date,_ozone,_temperature,_humidity,_hygrometry,_waterTemperature,_waterLevel,_probe]
        myinsertdb.insertIntoValue(parameter)

myinsertdb.close()

myquerydb = dataBase.sqlite3.QueryDb.DbQuery(path, name)
myquerydb.query()
myquerydb.close()

#os.remove((path + name))