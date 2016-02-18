#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

#création d'une connexion a la base de donnée des balise
connection = sqlite3.connect("../resources/Balise.db")

#création d'un curseur pour interagir avec la basse de donnée
cursor = connection.cursor()

#création de la table balise dans la basse de donnée
cursor.execute('''CREATE TABLE `balise` (
                  `b_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  `b_nom`	INTEGER NOT NULL UNIQUE
                  )''')

#création de la table releve dans la base de donnee et liaison entre balise et relevee
cursor.execute(''' CREATE TABLE `releve` (
                  `r_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  `r_date`	NUMERIC NOT NULL,
                  `r_ozone`	INTEGER NOT NULL,
                  `r_temperature`	REAL NOT NULL,
                  `r_humidite`	REAL NOT NULL,
                  `r_hygrometrie`	REAL NOT NULL,
                  `r_balise`	INTEGER NOT NULL,
                  FOREIGN KEY(`r_balise`) REFERENCES balise(`b_id`)
                  )''')

#sauvgarde des donnée
connection.commit()

#fermeture de la connection a la base de donnée
connection.close()