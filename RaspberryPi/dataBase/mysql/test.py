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
import ConnectMysqlDb
import CreateMysqlTable
import random
import time

myconnect = ConnectMysqlDb.ConnectMysqlDb("localhost","root","azerty","smartforest")
myconnect.connect()

#init
createTable = CreateMysqlTable.CreateMysqlTable()
myInsert = InsertMysqlDB.InsertMysqlDB()

#creation des table de la bdd
createTable.createTable()

for command in createTable.getSQL():
    myconnect.sendCommand(command)

#preparation insert sensortype

myInsert.insertIntoSensorType("ozone")
myInsert.insertIntoSensorType("temperature")
myInsert.insertIntoSensorType("airHumidity")
myInsert.insertIntoSensorType("groundHumidity")
myInsert.insertIntoSensorType("waterLevel")
myInsert.insertIntoSensorType("waterTemperature")

#preparation insert station
for a in range(0,9):

    namestation = "station " + str(a)
    latitude = 42.674475
    longitude = 2.847765
    installdate = time.time()

    myInsert.insertIntoStation(namestation,longitude, latitude,installdate)

#preparation insert sensor
for b in range(1,4):
    for c in range(1,10):
        myInsert.insertIntoSensor(c,b)

#preparation insert measure
for d in range(1,100):

        date = time.time()
        ozone = random.uniform(40,70)
        temperature = random.uniform(20,30)
        airHumidity = random.uniform(10,60)
        groundHumidity = random.uniform(10,60)

        myInsert.insertIntoMeasure(date,ozone,1)
        myInsert.insertIntoMeasure(date,temperature,2)
        myInsert.insertIntoMeasure(date,airHumidity,3)
        myInsert.insertIntoMeasure(date,groundHumidity,4)
        time.sleep(1)

#execution de toute les commande insert
for command in myInsert.getSQL():

    print command
    myconnect.sendCommand(command)


myconnect.close()
