#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConnectDB
import sqlite3

class CreateDB(ConnectDB.ConnectDB):
    def __init__(self,path,name):
        ConnectDB.ConnectDB.__init__(self,path,name)
        self.connect()

    def create(self):
        # création de la table balise dans la basse de donnée
        try:
            self.cursor.execute('''CREATE TABLE `probe` (
                                                   `p_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                   `p_name`	INTEGER NOT NULL UNIQUE
                                                   )''')
        except sqlite3.OperationalError:
            print"Table `probe` already exists"

        #print "Table `probe` created"

        # création de la table monitoring dans la basse de donnée
        try:
            self.cursor.execute(''' CREATE TABLE `value` (
                                                    `v_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                                    `v_date`	NUMERIC NOT NULL,
                                                    `v_ozone`	REAL NOT NULL,
                                                    `v_temperature`	REAL NOT NULL,
                                                    `v_groundHumidity`	REAL NOT NULL,
                                                    `v_airHumidity`	REAL NOT NULL,
                                                    `v_probe`	INTEGER NOT NULL,
                                                    FOREIGN KEY(`v_probe`) REFERENCES probe(`p_id`)
                                                    )''')
        except sqlite3.OperationalError:
            print"Table `value` already exists"

        #print "Table `value` created"
        #print "Database is ready to use"

        self.close()