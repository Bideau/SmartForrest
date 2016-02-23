#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import sqlite3


# ======================================================================================================================#
# fonction de création de la basse de donnée
# ======================================================================================================================#
def createDataBase(path, name):
    # création d'une connexion a la base de donnée
    connection = sqlite3.connect(path + name)

    # création d'un curseur pour interagir avec la basse de donnée
    cursor = connection.cursor()

    # création de la table balise dans la basse de donnée
    cursor.execute('''CREATE TABLE `probe` (
                      `p_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                      `p_name`	INTEGER NOT NULL UNIQUE
                      )''')

    # création de la table releve dans la base de donnee et liaison entre balise et relevee
    cursor.execute(''' CREATE TABLE `monitoring` (
                    `m_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                    `m_date`	NUMERIC NOT NULL,
                    `m_ozone`	INTEGER NOT NULL,
                    `m_temperature`	REAL NOT NULL,
                    `m_humidity`	REAL NOT NULL,
                    `m_hygrometry`	REAL NOT NULL,
                    `m_probe`	INTEGER NOT NULL,
                    FOREIGN KEY(`m_probe`) REFERENCES probe(`p_id`)
                    )''')
    # sauvgarde des donnée
    connection.commit()

    datetime.fromtimestamp(datetime)

    # fermeture de la connection a la base de donnée
    connection.close()


# ======================================================================================================================#
# fonction d'enregistrement de donnée dans la table balise
# ======================================================================================================================#
def inserIntoBalise(path, name, id, balise, monitoring):
    # création d'une connexion a la base de donnée
    connection = sqlite3.connect(path + name)

    # création d'un curseur pour interagir avec la basse de donnée
    cursor = connection.cursor()

    inserInto = "INSERT INTO monitoring VALUES (" + str(monitoring.getId()) + "," \
                + ",?,?,?,?)"

    cursor.executemany()
