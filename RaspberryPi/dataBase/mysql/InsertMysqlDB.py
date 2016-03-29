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

import SqlCommand

class InsertMysqlDB(SqlCommand.SqlCommand):

    def __init__(self):
        self.sqlCommand = []

    def insertIntoSensorType(self,sensorType):

        command = "INSERT INTO sensorType(st_type) VALUE ('" + sensorType + "');"
        self.sqlCommand.append(command)

    def insertIntoSensor(self,id_station,id_sensorType):
        command = "INSERT INTO sensor(st_id,sta_id) VALUE (" + str(id_sensorType) + "," + str(id_station) + ");"
        self.sqlCommand.append(command)

    def insertIntoStation(self,name,longitude,latitude,installDate):
        command = "INSERT INTO station(sta_name, sta_longitude, sta_latitude, sta_installDate) VALUE "\
                                     "('" + name + "'," + str(longitude) + "," + str(latitude) + "," + str(installDate) + ");"
        self.sqlCommand.append(command)

    def insertIntoMeasure(self,date,value,s_id):

        command = "INSERT INTO measure(m_date, m_value, s_id) VALUE (" + str(date) + "," + str(value) + "," + str(s_id) + ");"
        self.sqlCommand.append(command)

    def insertIntoUser(self,lastName,firstName,description):
        command = "INSERT INTO user(u_lastName, u_firstName, u_description) VALUE "\
                                  "('" + lastName + "', '" + firstName + "', '" + description + "');"
        self.sqlCommand.append(command)

    def insertIntoConnection(self,userId,login, password, adminKey):
        if (adminKey == None):
            command = "INSERT INTO connection(u_id, c_login, c_password) VALUE "\
                                            "('" + userId + "', '" + login + "', '" + password + "');"
        else:
            command = "INSERT INTO connection(u_id, c_login, c_password, c_adminKey) VALUE "\
                                            "('" + userId + "', '" + login + "', '" + password + "', '" + adminKey + "');"
        self.sqlCommand.append(command)

    def insertIntoStationAccess(self,userId,stationId):
        command = "INSERT INTO stationAccess(u_id, sta_id) VALUE "\
                                           "(" + userId + "," + stationId + ");"
        self.sqlCommand.append(command)

    def getSQL(self):

        return self.sqlCommand