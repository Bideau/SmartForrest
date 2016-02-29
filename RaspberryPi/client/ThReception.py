#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading
import string

## TODO DOCUMENTATION DES CLASSE DU CLIENT

class ThReception(threading.Thread):

    """objet thread gérant la réception des messages"""
    def __init__(self, connection,thE):
        threading.Thread.__init__(self)
        self.connection = connection  # ref. du socket de connexion
        self.thE = thE #ref. du thread d'émission
        self.msgReceived = ""

    def run(self):
        while 1:
            self.msgReceived = self.connection.recv(1024)
            self.msgReceived = string.replace(self.msgReceived, '\n', '')
            print "msgServer : " + self.msgReceived

            if self.msgReceived == '' or self.msgReceived.upper() == "FIN":
                break
                # Le thread <réception> se termine ici.
                # On force la fermeture du thread <émission> :

        self.thE._Thread__stop()
        #référence au thread d'emission, obligation de l'appeler thEmission

        print("client stoped, broken connection")
        self.connection.close