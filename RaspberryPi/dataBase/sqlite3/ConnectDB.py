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

__author__ = "Christophe Aubert"
__version__ = "1.0"


import dataBase.sqlite3

class ConnectDB(object):
    """
    Class connect db est une classe abstraite qui permet de se connecter a une base de donnée sqlite3
    """
    def __init__(self, path, name):
        """
        Init
        @param path:
        @param name:
        """
        self.path = path
        self.name = name
        self.connection = None
        self.cursor = None

    def connect(self):
        """
        Méthode de création d'une connexion a la base de donnée
        """
        self.connection = dataBase.sqlite3.connect(self.path + self.name)
        self.connection.row_factory = dataBase.sqlite3.Row #facilite la vie pour le traitement des données
        self.cursor = self.connection.cursor() # création d'un curseur pour interagir avec la basse de donnée

    def close(self):
        """
        Méthode qui permet de fermé une basse de données
        """
        self.connection.commit()
        self.connection.close()