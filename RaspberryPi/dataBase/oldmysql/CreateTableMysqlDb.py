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

import ConnectMysqlDb
import mysql.connector.errors

class CreateTableMysqlDb(ConnectMysqlDb.ConnectMysqlDb):

    def __init__(self,host,user,password,nameDb):
        ConnectMysqlDb.ConnectMysqlDb.__init__(self,host,user,password,nameDb)
        self.connect()

    def createTableSensortType(self):
        """
        Méthode de création de la table SensorType dans la basse de donnée
        """
        print "debut de creation table"
        try:
            #------------------------------------------------------------
            # Table: sensorType
            #------------------------------------------------------------
            self.cursor.execute('''CREATE TABLE sensorType(
                                            st_id   int (11) Auto_increment  NOT NULL ,
                                            st_type Varchar (50) NOT NULL ,
                                            PRIMARY KEY (st_id )
                                   )ENGINE=InnoDB;''')
            print"Table sensorType is created"

        except mysql.connector.errors.OperationalError:
            print"Table `sensorType` already exists."

        try:
            #------------------------------------------------------------
            # Table: station
            #------------------------------------------------------------
            self.cursor.execute('''CREATE TABLE station(
                                            sta_id        int (11) Auto_increment  NOT NULL ,
                                            sta_name      Varchar (50) NOT NULL ,
                                            sta_longitude Float NOT NULL ,
                                            PRIMARY KEY (sta_id )
                                   )ENGINE=InnoDB;''')
            print"Table station is created"

        except mysql.connector.errors.OperationalError:
            print"Table `sensorType` already exists."

        try:
            self.cursor.execute('''CREATE TABLE sensorType(
                                        st_id   int (11) Auto_increment  NOT NULL ,
                                        st_type Varchar (50) NOT NULL ,
                                        PRIMARY KEY (st_id )
                                )ENGINE=InnoDB;''')
            print"Table sensorType is created"

        except mysql.connector.errors.OperationalError:
            print"Table `sensorType` already exists."

