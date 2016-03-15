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


class DeleteTableDb(ConnectDB.ConnectDB):
    """
    Class DeleteTableDb permet de supprimer les valeurs dans la base de donnée
    """
    def __init__(self, path, name):
        """
        Init

        @param path:
        @param name:
        """
        ConnectDB.ConnectDB.__init__(self, path, name)
        self.connect()

    def deleteFromProbe(self):
        """
         Méthode qui permet de surppriser toute les valeur de la table probe
        """
        self.cursor.execute("DELETE FROM probe")
        self.cursor.execute("VACUUM")
        print" Data in probe are delete."

    def deleteFromValue(self):
        """
         Méthode qui permet de surppriser toute les valeur de la table value
        """
        self.cursor.execute("DELETE FROM value")
        self.cursor.execute("VACUUM")
        print "Data in value are delete."