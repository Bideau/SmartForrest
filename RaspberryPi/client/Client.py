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


import ThEmission
import ThReception
import socket
import sys

class Client(object):
    """
    Classe client
    """

    def __init__(self,host,port):
        """
        init

        @param host:
        @param port:

        """
        self.host = host # adresse du serveur
        self.port = port # port de connection au serveur
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        try:
            self.socket.connect((host,port)) #connection au serveur
            print "Connection on " + host + " {}".format(port) + "."

        except socket.error:
            print "connection failed."
            sys.exit() #arret du client

        self.thE = ThEmission.ThEmission(self.socket) #création du du thread d'émission
        self.thR = ThReception.ThReception(self.socket,self.thE) #création du thread de réception

        #démarage des threads
        self.thE.start()
        self.thR.start()

    def sendMsg(self,msg):

        """
        Methode pour envoyé les message au serveur

        @param msg:

        """

        self.thE.sendMsg(msg)
