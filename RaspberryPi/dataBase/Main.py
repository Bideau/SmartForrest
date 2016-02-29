#!/usr/bin/python
# -*- coding: utf-8 -*-

import CreateDB
import InsertDb
import DeleteTableDb
import QueryDb
import time
import random
import os
path = "../ressources/"
name = "db.db"
rangeP = 100
rangeV = 10000

#creation de la db
mydb = CreateDB.CreateDB(path,name)
mydb.create()

#insertion data
myinsertdb = InsertDb.InsertDb(path,name)

for i in range(0,rangeP):
    _name = "probe " + str(i)
    parameter = [_name]
    myinsertdb.insertIntoProbe(parameter)

#insert dans value
for i in range(0,rangeP):
    for j in range(0,rangeV):
        _date = time.time()
        _ozone = random.uniform(40,70)
        _temperature = random.uniform(20,30)
        _humidity = random.uniform(10,60)
        _hygrometry = random.uniform(10,60)
        _probe = j
        parameter = [_date,_ozone,_temperature,_humidity,_hygrometry,_probe]
        myinsertdb.insertIntoValue(parameter)

myinsertdb.close()

myquerydb =QueryDb.DbQuery(path,name)
myquerydb.query()
myquerydb.close()

#os.remove((path + name))