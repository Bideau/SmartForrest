#!/usr/bin/python
# -*- coding: utf-8 -*-

import Client

## programme

# La Ligne suivante permet de s'assurer de lancer correctement le programme à son appel
# if __name__ == "__main__":

host = "172.30.0.206" #quentin
#host = "172.30.0.103"

#port = 8080 #quentin
port = 8081

myclient = Client.Client(host,port)
myclient.sendMsg("toto is back")