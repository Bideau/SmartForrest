#!/usr/bin/python
# -*- coding: utf-8 -*

import ConnectDB

class DeleteTableDb(ConnectDB.ConnectDB):
    def __init__(self, path, name):
        ConnectDB.ConnectDB.__init__(self,path,name)
        self.connect()

    def deleteFromProbe(self):
        self.cursor.execute("DELETE FROM probe")
        self.cursor.execute("VACUUM")

    def deleteFromValue(self):
        self.cursor.execute("DELETE FROM value")
        self.cursor.execute("VACUUM")