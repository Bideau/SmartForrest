#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time

from dataBase.noDB import JsonFile
from dataBase.sqlite3 import ProbeData

json = JsonFile.JsonFile()

for _i in range(0,144):
    _date = time.time()
    _ozone = random.uniform(40,70)
    _temperature = random.uniform(20,30)
    _groudHumidity = random.uniform(10, 60)
    _airHumidity = random.uniform(10,60)

    _probeData = ProbeData.ProbeData()
    _probeData.setValue(_i,
                        _date,
                        _ozone,
                        _temperature,
                        _groudHumidity,
                        _airHumidity)

    json.addData(_probeData.toJson())
    #json.addData("toto ")

json.writeToJson()