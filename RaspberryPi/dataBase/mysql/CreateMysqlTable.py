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

class CreateMysqlTable(SqlCommand.SqlCommand):

    def __init__(self):

        self.sqlCommand = []

    def createTable(self):

        # Table: sensorType
        #------------------------------------------------------------
        sensorType = "CREATE TABLE sensorType( "\
                                  "st_id   INT (11) Auto_increment  NOT NULL ,"\
                                  "st_type VARCHAR (50) NOT NULL ,"\
                                  "PRIMARY KEY (st_id )"\
                     ")ENGINE=InnoDB;"
        self.sqlCommand.append(sensorType)

        #------------------------------------------------------------
        # Table: measure
        #------------------------------------------------------------

        measure = "CREATE TABLE measure( "\
                               "m_id    INT (11) Auto_increment  NOT NULL ,"\
                               "m_date  INT NOT NULL ,"\
                               "m_value FLOAT NOT NULL ,"\
                               "s_id    INT NOT NULL ,"\
                               "PRIMARY KEY (m_id )"\
                  ")ENGINE=InnoDB;"
        self.sqlCommand.append(measure)

        #------------------------------------------------------------
        # Table: sensor
        #------------------------------------------------------------

        sensor = "CREATE TABLE sensor( "\
                              "s_id   INT (11) Auto_increment  NOT NULL , "\
                              "st_id  INT NOT NULL , "\
                              "sta_id INT NOT NULL , "\
                              "PRIMARY KEY (s_id ) "\
                 ")ENGINE=InnoDB;"
        self.sqlCommand.append(sensor)

        #------------------------------------------------------------
        # Table: station
        #------------------------------------------------------------

        station = "CREATE TABLE station( "\
                               "sta_id        INT (11) Auto_increment  NOT NULL , "\
                               "sta_name      VARCHAR (50) NOT NULL , "\
                               "sta_longitude FLOAT NOT NULL , "\
                               "sta_latitude  FLOAT NOT NULL, "\
                               "sta_installDate INT NOT NULL, "\
                               "PRIMARY KEY (sta_id ) "\
                  ")ENGINE=InnoDB;"
        self.sqlCommand.append(station)

        #------------------------------------------------------------
        # Table: user
        #------------------------------------------------------------

        user = "CREATE TABLE user ( "\
                            "u_id          INT (11) Auto_increment NOT NULL,"\
                            "u_lastName    VARCHAR(30) NOT NULL,"\
                            "u_firstName   VARCHAR(30) NOT NULL,"\
                            "u_description VARCHAR(200) NOT NULL,"\
                            "PRIMARY KEY (u_id)"\
               ")ENGINE=InnoDB;"
        self.sqlCommand.append(user)

        #------------------------------------------------------------
        # Table: connection
        #------------------------------------------------------------
        connection = "CREATE TABLE connection ( "\
                                  "c_id       INT (11) Auto_increment NOT NULL,"\
                                  "u_id       INT NOT NULL,"\
                                  "c_login    VARCHAR(30) NOT NULL,"\
                                  "c_password VARCHAR (50) NOT NULL ,"\
                                  "c_adminKey BOOLEAN DEFAULT NULL,"\
                                  "PRIMARY KEY(c_id)"\
                     ")ENGINE=InnoDB;"
        self.sqlCommand.append(connection)

        stationAccess = "CREATE TABLE stationAccess ( "\
                                      "staa_id INT (11) Auto_increment NOT NULL,"\
                                      "u_id INT NOT NULL ,"\
                                      "sta_id INT NOT NULL ,"\
                                      "PRIMARY KEY(staa_id)"\
                        ")ENGINE=InnoDB;"
        self.sqlCommand.append(stationAccess)
        #------------------------------------------------------------
        # ALTER TABLE
        #------------------------------------------------------------

        atMeasure = "ALTER TABLE measure ADD CONSTRAINT FK_measure_s_id "\
                                        "FOREIGN KEY (s_id) REFERENCES sensor(s_id);"
        self.sqlCommand.append(atMeasure)

        atsensor = "ALTER TABLE sensor ADD CONSTRAINT FK_sensor_st_id "\
                                      "FOREIGN KEY (st_id) REFERENCES sensorType(st_id);"
        self.sqlCommand.append(atsensor)

        atsensor2 = "ALTER TABLE sensor ADD CONSTRAINT FK_sensor_sta_id "\
                                       "FOREIGN KEY (sta_id) REFERENCES station(sta_id);"
        self.sqlCommand.append(atsensor2)

        atConnection = "ALTER TABLE connection  ADD CONSTRAINT FK_connection_u_id "\
                                               "FOREIGN KEY (u_id) REFERENCES user(u_id)"
        self.sqlCommand.append(atConnection)

        atstationAccess  = "ALTER TABLE stationAccess ADD CONSTRAINT FK_stationAccess_u_id "\
                                                     "FOREIGN KEY (u_id) REFERENCES user(u_id)"
        self.sqlCommand.append(atstationAccess)

        atstationAccess2 = "ALTER TABLE stationAccess ADD CONSTRAINT FK_stationAccess_sta_id "\
                                                      "FOREIGN KEY (sta_id) REFERENCES station(sta_id)"
        self.sqlCommand.append(atstationAccess2)


    def getSQL(self):
        return self.sqlCommand