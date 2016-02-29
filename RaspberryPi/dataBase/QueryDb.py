#!/usr/bin/python
# -*- coding: utf-8 -*-

import ProbeData
import ConnectDB

class DbQuery(ConnectDB.ConnectDB):
    def __init__(self, path, name):
        ConnectDB.ConnectDB.__init__(self,path,name)
        self.connect()

    def query(self):
        _data = self.cursor.execute('''SELECT v_probe,
                                                v_date,
                                                v_ozone,
                                                v_temperature,
                                                v_groundHumidity,
                                                v_airHumidity FROM value''')

        _probeData = ProbeData.ProbeData()

        for row in _data:

            _probeData.setValue(row['v_probe'],row['v_date'],row['v_ozone'],row['v_temperature'],row['v_groundHumidity'],row['v_airHumidity'])
            #print _probeData.toJson()
