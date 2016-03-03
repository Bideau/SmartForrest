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

from dataBase.sqlite3 import ConnectDB


class InsertDb(ConnectDB.ConnectDB):
    """
    Classe InsertDb permet d'insérer les donnée dans la bdd sur les table probe et value
    """
    def __init__(self, path,name):
        """
        Constructeur de InsertDB

        @param path:
        @param name:
        """
        ConnectDB.ConnectDB.__init__(self, path, name)
        self.connect()

    def insertIntoProbe(self, tabParameter):
        """
        Méthode qui permet d'insérer les données la la table probe

        @param tabParameter: 1 parametre
        @return:
        """
        self.cursor.execute('INSERT INTO probe ('
                               'p_name,'
                               'p_longitude,'
                               'p_latitude) VALUES (?,?,?)', tabParameter)
        print"Insert data in probe table are finish"

    def insertIntoValue(self, tabParameter):
        """
        Méthode qui permet d'insérer les données la la table value

        @param tabParameter: tableau de 6 parametre v_date,v_ozone,v_temperature,v_groundHumidity,v_airHumidity,v_probe
        """
        self.cursor.execute('INSERT INTO value ('
                               'v_date,'
                               'v_ozone,'
                               'v_temperature,'
                               'v_groundHumidity,'
                               'v_airHumidity,'
                               'v_waterTemperature,'
                               'v_waterLevel,'
                               'v_probe) VALUES (?,?,?,?,?,?,?,?)', tabParameter)
        print"Insert data in value table are finish"
