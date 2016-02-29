#!/usr/bin/python
# -*- coding: utf-8 -*-

import ThEmission
import ThReception
import socket
import sys

class Client(object):

    def __init__(self,host,port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            self.socket.connect((host,port))
            print "Connection on " + host + " {}".format(port) + "."

        except socket.error:
            print "connection failed."
            sys.exit()

        self.thE = ThEmission.ThEmission(self.socket)
        self.thR = ThReception.ThReception(self.socket,self.thE)

        self.thE.start()
        self.thR.start()

    def sendMsg(self,msg):

        self.thE.sendMsg(msg)
