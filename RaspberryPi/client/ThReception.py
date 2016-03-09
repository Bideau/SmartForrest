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


import threading
import string

# Taille du buffer
global BUFFER
BUFFER = 1024

class ThReception(threading.Thread):

    """
    Class thread gérant l'émission des messages
    """

    def __init__(self, connection,thE):
        """
        init

        @param connection:
        @param thE:

        """
        threading.Thread.__init__(self)
        self.connection = connection  # ref. du socket de connexion
        self.thE = thE #ref. du thread d'émission
        self.msgReceived = ""

    def run(self):

        """
        Methode de lancement du thread
        """

        while 1:
            self.msgReceived = self.connection.recv(BUFFER) # reception du message
            self.msgReceived = string.replace(self.msgReceived, '\n', '')# supression du \n
            print "msgServer : " + self.msgReceived

            if self.msgReceived == '' or self.msgReceived.upper() == "FIN":
                break
                # Le thread <réception> se termine ici.
         # On force la fermeture du thread <émission> :
        self.thE._Thread__stop()

        print("client stoped, broken connection")

        self.connection.close # fermeture de la connection