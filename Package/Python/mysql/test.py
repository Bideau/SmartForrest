#!/usr/bin/python
# -*- coding: utf-8 -*

"""
The MIT License (MIT)
Copyright (c) 2015 Christophe Aubert
Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

__author__ = "Christophe Aubert"
__version__ = "1.0"

import InsertMysqlDB
import ConnectMysqlDB
import CreateMysqlTable
import random
import time

import QueryMysqlDB

PATH_SCRIPT="../../Script"
host=Popen(PATH_SCRIPT+"/GetInfo.sh HOST", stdout=PIPE, shell=True).stdout.read()
db=Popen(PATH_SCRIPT+"/GetInfo.sh DB", stdout=PIPE, shell=True).stdout.read()
password=Popen(PATH_SCRIPT+"/GetInfo.sh PASS", stdout=PIPE, shell=True).stdout.read()
user=Popen(PATH_SCRIPT+"/GetInfo.sh USER", stdout=PIPE, shell=True).stdout.read()

# host = "srvmysql.imerir.com"
# user = "SmartForest"
# password = "LjcX7vWRMs84jJ3h"
# db = "SmartForest"
# host = "localhost"
# user = "root"
# password = "azerty"
# db = "smartforest"

myconnect = ConnectMysqlDB.ConnectMysqlDB(host, user, password, db)
myconnect.connect()

#init
createTable = CreateMysqlTable.CreateMysqlTable()
myInsert = InsertMysqlDB.InsertMysqlDB()

#creation des table de la bdd
createTable.createTable()

for command in createTable.getSQL():
    myconnect.sendCommand(command)

#preparation user

myInsert.insertIntoUser("Admin","Admin", "Administrateur")
myInsert.insertIntoConnection("1","admin","21232f297a57a5a743894a0e4a801fc3", "1","0")

#preparation insert sensortype

myInsert.insertIntoSensorType("ozone")
myInsert.insertIntoSensorType("temperature")
myInsert.insertIntoSensorType("airHumidity")
myInsert.insertIntoSensorType("groundHumidity")
myInsert.insertIntoSensorType("waterLevel")
myInsert.insertIntoSensorType("waterTemperature")
"""
#preparation insert station
for station in range(0,10):

    namestation = "station " + str(station)
    latitude = 42.674475
    longitude = 2.847765
    installdate = 1454281200

    myInsert.insertIntoStation(namestation,longitude, latitude,installdate)
    stationId = 1 + station
    myInsert.insertIntoStationAccess("1", str(stationId))

#preparation insert sensor
#TODO revoir code probleme insert bdd
cptSensor = 0
for station in range(1,11):
    for sensor in range(1,5):
        cptSensor += 1
        myInsert.insertIntoSensor(station,sensor)


cptSensor += 1
print cptSensor


#preparation insert measure
# date = 1454281200
# cpt = 0
# for measures in range (0,10):
#     cpt+=1
#     for measure in range(1,cptSensor):
#
#         value = random.uniform(10,80)
#         myInsert.insertIntoMeasure(date,value,measure)
#     date += 360

date = 1454281200

for period in range(0,2400):

    print "iteration : " + str(period)
    #boucle for pour 1 enregistrement sur 10 station de 4 capteur
    cptsensor2 = 1
    for station in range(1,11):
        print "iteration station : " + str(station)
        #first station sensor
        ozone = random.uniform(10,80)
        myInsert.insertIntoMeasure(date,ozone,cptsensor2)
        cptsensor2 += 1
        #2
        temperature = random.uniform(20,30)
        myInsert.insertIntoMeasure(date,temperature,cptsensor2)
        cptsensor2 += 1
        #3
        airHumidity = random.uniform(15,40)
        myInsert.insertIntoMeasure(date,airHumidity,cptsensor2)
        cptsensor2 += 1
        #4
        groundHulidity  = random.uniform(10,35)
        myInsert.insertIntoMeasure(date,groundHulidity,cptsensor2)
        cptsensor2 += 1

    date += 360
"""
#execution de toute les commande insert
for command in myInsert.getSQL():

    print command
    myconnect.sendCommand(command)


# myquerry = QueryMysqlDB.QueryMysqlDB()
# myquerry.queryStation()
# print myquerry.getSQL()
# myconnect.sendQuery(myquerry.getSQL())
# row = myconnect.cursor.fetchall()

print
myconnect.close()
