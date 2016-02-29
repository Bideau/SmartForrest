#!/usr/bin/python
# -*- coding: utf-8 -*-

import sqlite3

class ConnectDB(object):
    def __init__(self, path, name):
        self.path = path
        self.name = name
        self.connection = None
        self.cursor = None

    def connect(self):
        # création d'une connexion a la base de donnée
        self.connection = sqlite3.connect(self.path + self.name)
        self.connection.row_factory = sqlite3.Row #facilite la vie pour le traitement des données

        # création d'un curseur pour interagir avec la basse de donnée
        self.cursor = self.connection.cursor()

    def close(self):
        self.connection.commit()
        self.connection.close()