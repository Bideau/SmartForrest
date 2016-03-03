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

import dataBase.sqlite3.ProbeData
from dataBase.sqlite3 import ConnectDB


class DbQuery(ConnectDB.ConnectDB):
    def __init__(self, path, name):
        ConnectDB.ConnectDB.__init__(self, path, name)
        self.connect()

    def query(self):
        _data = self.cursor.execute('''SELECT v_probe,
                                              v_date,
                                              v_ozone,
                                              v_temperature,
                                              v_groundHumidity,
                                              v_airHumidity FROM value''')

        _probeData = dataBase.sqlite3.ProbeData.ProbeData()

        for row in _data:

            _probeData.setValue(row['v_probe'],row['v_date'],row['v_ozone'],row['v_temperature'],row['v_groundHumidity'],row['v_airHumidity'])
            #print _probeData.toJson()
