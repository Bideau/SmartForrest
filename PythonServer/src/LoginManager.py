#! /usr/bin/env python

import sys
import MySQLdb as mdb
error=0

# Verification du login
def isLogin(login):
	valid = False
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			cur.execute("SELECT COUNT(*) FROM info_connexion where login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid = True

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)

	finally:
		con.close()
	print(valid)
	return valid

# Verification du mot de passe
def isPass(login, password):
	valid = False
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			cur.execute("SELECT motDePasse FROM info_connexion where login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == password):
					valid = True
				print(row)
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)

	finally:
		con.close()
	return valid

# Verification du login
def isBalise(capteurId):
	valid = False
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			cur.execute("SELECT COUNT(*) FROM info_balise where idBalise=\'%s\'" % capteurId)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid = True

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)

	finally:
		con.close()
	print(valid)
	return valid

# Insert un utilisateur et un login dans la BDD
def insertUser(login, password, nom, prenom, desc):
	global UserId
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			print("toto")
			print("fuck")
			cur.execute("INSERT INTO info_utilisateur values (NULL,\'"+nom+"\',\'"+prenom+"\',\'"+desc+"\')")
			print("toto1")
			cur.execute("SELECT idUser FROM info_utilisateur where nom=\'"+nom+"\' AND prenom=\'"+prenom+"\' AND description=\'"+desc+"\'")
			print("toto2")
			UserId=0
			rows = cur.fetchall()
			for row in rows:
				print(row)
				UserId = row[0]
				print (UserId)
			print("Salope")
			print("INSERT INTO info_connexion values (NULL,\'"+str(UserId)+"\',\'"+login+"\',\'"+password+"\',False)")
			print("Pute")
			cur.execute("INSERT INTO info_connexion values (NULL,\'"+str(UserId)+"\',\'"+login+"\',\'"+password+"\',False)")

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		return 1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		return 1000
	finally:
		con.close()
	return 200

# retourne les information de l'utilisateur du login
def userInfo(login):
	tmp={"nom":"toto","prenom":"toto","description":"toto","login":login}
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			cur.execute("SELECT iu.nom,iu.prenom,iu.description FROM info_connexion ic INNER JOIN info_utilisateur iu "+
						"ON iu.idUser=ic.idUSer where ic.login=\'"+str(login)+"\' ")
			rows = cur.fetchone()

			nom=rows[0]
			prenom=rows[1]
			desc=rows[2]
			tmp["nom"]=nom
			tmp["prenom"]=prenom
			tmp["description"]=desc
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return tmp

# retourne les information de l'utilisateur du login
def userAccess(login,capteurId):
	valid=False
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			cur.execute("SELECT Count(ib.idBalise) FROM info_balise ib "+
						"INNER JOIN acces_balise ab ON ab.idBalise=ib.idBalise "+
						"INNER JOIN info_utilisateur iu ON iu.idUser=ab.idUser "+
						"INNER JOIN info_connexion ic ON iu.idUser=ic.idUser "+
						"where ic.login=\'"+str(login)+"\' AND ib.idBalise=\'"+str(capteurId)+"\' ")
			#rows = cur.fetchone()
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid = True
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return valid

# Retourne les valeurs des capteurs d'une balise entre 2 dates
def capteurValue(login,capteurId,dateDebut,dateFin):
	myArray=[]
	try:
		con = mdb.connect('srvmysql.imerir.com', 'SmartForest', 'LjcX7vWRMs84jJ3h', 'SmartForest')
		with con:
			cur = con.cursor()
			print("SELECT dl.hygrometrie,dl.temperature,dl.ozone,dl.humidite, dl.dateReleve FROM donnees_lora dl "+
						"INNER JOIN info_balise ib ON ib.idBalise=dl.idBalise "+
						"INNER JOIN acces_balise ab ON ab.idBalise=ib.idBalise "+
						"INNER JOIN info_utilisateur iu ON iu.idUser=ab.idUser "+
						"INNER JOIN info_connexion ic ON iu.idUser=ic.idUser "+
						"where ic.login=\'"+str(login)+"\' AND ib.idBalise=\'"+str(capteurId)+"\' "+
								"AND \'"+str(dateDebut)+"\'<= dl.dateReleve AND \'"+str(dateFin)+"\'>= dl.dateReleve")
			cur.execute("SELECT dl.hygrometrie,dl.temperature,dl.ozone,dl.humidite, dl.dateReleve FROM donnees_lora dl "+
						"INNER JOIN info_balise ib ON ib.idBalise=dl.idBalise "+
						"INNER JOIN acces_balise ab ON ab.idBalise=ib.idBalise "+
						"INNER JOIN info_utilisateur iu ON iu.idUser=ab.idUser "+
						"INNER JOIN info_connexion ic ON iu.idUser=ic.idUser "+
						"where ic.login=\'"+str(login)+"\' AND ib.idBalise=\'"+str(capteurId)+"\' "+
								"AND \'"+str(dateDebut)+"\'<= dl.dateReleve AND \'"+str(dateFin)+"\'>= dl.dateReleve")


			rows = cur.fetchall()
			for row in rows:
				tmp={"hygrometrie":"toto","temperature":"toto","ozone":"toto","humidite":"toto","dateReleve":"toto"}
				hygrometrie=row[0]
				temperature=row[1]
				ozone=row[2]
				humidite=row[3]
				dateReleve=row[4]

				tmp["hygrometrie"]=float(str(hygrometrie))
				tmp["temperature"]=float(str(temperature))
				tmp["ozone"]=float(str(ozone))
				tmp["humidite"]=float(str(humidite))
				tmp["dateReleve"]=dateReleve
				myArray.append(tmp)

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return myArray

# Retourne les valeurs d'ozone du capteur entre 2 dates
def ozoneValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		tmp["mesure"]=dic["ozone"]
		tmp["dateReleve"]=dic["dateReleve"]
		retour.append(tmp)
	return retour

# Retourne les valeurs d'hygrometrie du capteur entre 2 dates
def hygrometrieValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		tmp["mesure"]=dic["hygrometrie"]
		tmp["dateReleve"]=dic["dateReleve"]
		retour.append(tmp)
	return retour

# Retourne les valeurs de temperature du capteur entre 2 dates
def temperatureValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		tmp["mesure"]=dic["temperature"]
		tmp["dateReleve"]=dic["dateReleve"]
		retour.append(tmp)
	return retour

# Retourne les valeurs d'humidite du capteur entre 2 dates
def humiditeValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		tmp["mesure"]=dic["humidite"]
		tmp["dateReleve"]=dic["dateReleve"]
		retour.append(tmp)
	return retour