#!/usr/bin/env python
# Definition d'un serveur reseau rudimentaire
# Ce serveur attend la connexion d'un client, pour entamer un dialogue avec lui

import socket, sys,json
import MySQLdb as mdb

#probeID
#date
#ozone
#temperature
#hygrometrie
#humidity
def parsing(myJSON):
	try:
		req_data = json.loads(myJSON)
		# recuperation du probeID
		probeID = req_data["probeID"]
		# recuperation de la valeur d'ozone
		ozone = req_data["ozone"]
		# recuperation de la valeur de temperature
		temperature = req_data["mesure"]
		# recuperation de la valeur d'hygrometrie
		hygrometrie = req_data["hygrometrie"]
		# recuperation de la valeur de humidite
		humidity = req_data["humidity"]
		# recuperation de date
		date = req_data["date"]
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			print("toto")
			print("fuck")
			cur.execute("INSERT INTO donnes_lora values (NULL,\'"+str(probeID)+"\',\'"+str(temperature)+"\',\'"+str(ozone)+"\',"+
															"\'"+str(humidity)+"\',\'"+str(date)+"\',\'"+str(hygrometrie)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000


def socketServer(threadName,HOST,PORT):
	print ("%s : %s:%s" % ( threadName,str(HOST),str(PORT) ))

	# 1) creation du socket :
	mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# 2) liaison du socket a une adresse precise :
	try:
		mySocket.bind((HOST, PORT))
	except socket.error:
		print ("La liaison du socket a l'adresse choisie a echoue.")
		sys.exit()
	while 1:
		# 3) Attente de la requete de connexion d'un client :
		print ("Serveur pret, en attente de requetes ...")
		mySocket.listen(5)

		# 4) Etablissement de la connexion :
		connexion, adresse = mySocket.accept()
		print ("Client connecte, adresse IP %s, port %s" % (adresse[0], adresse[1]))

		# 5) Dialogue avec le client :
		connexion.send("Vous etes connecte au serveur Toto. Envoyez vos messages.")
		msgClient = connexion.recv(1024)
		#while 1:
		print (msgClient)
		parsing(msgClient)
		#if msgClient.upper() == "FIN" or msgClient =="":
		#	break
		#msgServeur = raw_input("S> ")
		msgServeur="FIN"
		connexion.send(msgServeur)
		msgClient = connexion.recv(1024)

		# 6) Fermeture de la connexion :
		connexion.send("Au revoir !")
		print ("Connexion interrompue.")
		connexion.close()

		#ch = raw_input("<R>ecommencer <T>erminer ? ")
		#if ch.upper() =='T':
		#	break