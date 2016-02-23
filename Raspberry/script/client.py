#!/usr/bin/python
# -*- coding: utf-8 -*-

# TODO CREDIT
# http://python.developpez.com/cours/TutoSwinnen/?page=page_20


import socket
import string
import threading
from Tkinter import *

# host = "192.168.1.21" #quentin
host = "192.168.1.22"  # bideau
port = 8081


class ThRecepetion(threading.Thread):
    """objet thread gérant la réception des messages"""

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection  # ref. du socket de connexion

    def run(self):
        while 1:
            msgReceived = self.connection.recv(1024)
            msgReceived = string.replace(msgReceived, '\n', '')
            print "msgServer : " + msgReceived

            if msgReceived == '' or msgReceived.upper() == "FIN":
                break
                # Le thread <réception> se termine ici.
                # On force la fermeture du thread <émission> :
        thEmission._Thread__stop()

        print("Client stoped, broken connection")
        self.connection.close


class ThEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""

    def __init__(self, connection):
        threading.Thread.__init__(self)
        self.connection = connection

    def run(self):
        while 1:
            self.connection.send()
            msgSended = raw_input('Enter your msg : ')
            self.connection.send(msgSended)

    def sendMsg(self, msg):
        print("toto")
        self.connection.send(msg)


# Programme principal - Établissement de la connexion :
conect = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    conect.connect((host, port))
    print "Connection on " + host + " {}".format(port)
except socket.error:
    print("La connexion a échoué.")
    sys.exit()
print ("Connexion établie avec le serveur.")

thEmission = ThEmission(conect)
thReception = ThRecepetion(conect)
# thEmission.start()
thReception.start()
thEmission.sendMsg("toto")
