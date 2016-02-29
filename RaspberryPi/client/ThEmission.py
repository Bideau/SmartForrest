#!/usr/bin/python
# -*- coding: utf-8 -*-

import threading

class ThEmission(threading.Thread):
    """
    objet thread gérant l'émission des messages
    """
    def __init__(self, connection):
        super(ThEmission, self).__init__()
        threading.Thread.__init__(self)
        self.connection = connection
        self.msgsended = ""

    def run(self):
        while 1:
            # self.msgsended = raw_input('Enter your msg : ')
            # self.connection.send(self.msgsended)
            pass

    def sendMsg(self):
        self.connection.send(self.msgsended)

    def sendMsg(self, msg):
        self.msgsended = msg
        self.connection.send(self.msgsended)