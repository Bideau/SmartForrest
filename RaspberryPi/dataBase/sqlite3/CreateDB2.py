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

import dataBase.sqlite3

from dataBase.sqlite3 import ConnectDB


class CreateDB2(ConnectDB.ConnectDB):
    """
    Classe CreateDb permet de création de la basse de données avec toute ces tables
    """
    def __init__(self,path,name):
        """
        Init
        @param path:
        @param name:

        """
        ConnectDB.ConnectDB.__init__(self, path, name)
        self.connect()

    def create(self):
        """
        Méthode de création des tables dans la basse de donnée
        """
        # création de la table probe dans la basse de donnée
        try:
            self.cursor.execute('''CREATE TABLE `sensorType` (
                                                   `st_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                   `st_type` TEXT NOT NULL UNIQUE
                                                   )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `probe` already exists."

        # création de la table value dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `Probe` (
                                                    `d_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `d_date` REAL NOT NULL,
                                                    `d_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`d_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

        # création de la table ozone dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `ozone` (
                                                    `o_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `o_value` REAL NOT NULL,
                                                    `o_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`o_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

        # création de la table temperature dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `temperature` (
                                                    `t_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `t_value` REAL NOT NULL,
                                                    `t_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`t_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

        # création de la table groundHumidity dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `groundHumidity` (
                                                    `g_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `g_value` REAL NOT NULL,
                                                    `g_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`g_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

        # création de la table airHumidity dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `airHumidity` (
                                                    `a_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `a_value` REAL NOT NULL,
                                                    `a_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`a_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

         # création de la table waterTemperature dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `waterTemperature` (
                                                    `wt_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `wt_value` REAL NOT NULL,
                                                    `wt_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`wt_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

         # création de la table monitoring dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `waterLevel` (
                                                    `wl_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `wl_value` NUMERIC NOT NULL,
                                                    `wl_probe` INTEGER NOT NULL,
                                                    FOREIGN KEY(`wl_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except dataBase.sqlite3.OperationalError:
            print"Table `value` already exists."

        print"Data base ready to use."


        self.close()