#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import json
import sys
import os
import time


def parsingData():

    data = []

    buffer = open("buffer","r")

    for line in buffer:
        data.append(line.replace("\n", ""))

    buffer.close()
    #deleteBuffer()

    data = splitData(data,";")

    data = splitData(data,":")

    return data

def splitData(data, spliter):

    tmpdata = []
    dataSplited = []

    for dat in data:
        tmpdata.append(dat.split(spliter))

    for couples in tmpdata:
        for couple in couples:
            dataSplited.append(couple)

    return dataSplited

def reformatData(confPath, data):

    jsonFile = open(confPath, "r")
    jsondata = json.load(jsonFile)
    jsonFile.close()

    keys = jsondata.keys()
    cpt = 0

    for dat in data:
        if dat in keys:
            data[cpt] = str(jsondata[dat])
        cpt+=1

def deleteBuffer():
    os.remove("buffer")

def toJsonFile(filePath, data):

    jsonFile = open(filePath, "w")

    date = time.time()

    jsondata = "["


    for i in range(0,len(data)-1,2):

        if ( data[i] == "PROBE" and i == 0):
            jsondata += "{"

        if ( data[i] == "PROBE" and i > 0):
            jsondata += "},{"

        jsondata += "\"" + data[i] + "\":\"" + data[i+1] + "\""

        if (data[i] == "PROBE"):
            jsondata += ",\"DATE\":\"" + str(date) + "\""

        if ( i != len(data)-3 and data[i+2] != "PROBE"):
             jsondata += ","

    jsondata += "}]"

    jsonFile.write(jsondata)

    print jsondata

##############################

toto = parsingData()

reformatData("sensor.json", toto)

toJsonFile("data.json",toto)

print toto