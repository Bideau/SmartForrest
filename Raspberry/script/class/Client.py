#!/usr/bin/python
# -*- coding: utf-8 -*-
import threading


class Recepetion(threading.Thread):
    """objet thread gérant la réception des messages"""

    def __init__(self, connexion):
        threading.Thread.__init__(self)
        self.connexion = connexion  # ref. du socket de connexion

    def run(self):
        while 1:
            msgReceive = self.connexion.recv(1024)
            print "msgServer : " + msgReceive

            if msgReceive == '' or msgReceive.upper() == "FIN":
                break
            # Le thread <réception> se termine ici.
            # On force la fermeture du thread <émission> :
            thread
