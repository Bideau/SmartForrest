#!/usr/bin/python
# -*- coding: utf-8 -*-

import random
import time

from dataBase.noDB import JsonFile
from dataBase.sqlite3 import ProbeData

json = JsonFile.JsonFile()

for _i in range(0,144):
    date = time.time()
    ozone = random.uniform(40,70)
    temperature = random.uniform(20,30)
    groudHumidity = random.uniform(10, 60)
    airHumidity = random.uniform(10,60)

    probeData = ProbeData.ProbeData()
    probeData.setValue(_i,
                        date,
                        ozone,
                        temperature,
                        groudHumidity,
                        airHumidity)

    json.addData(probeData.toJson())

json.writeToJson()