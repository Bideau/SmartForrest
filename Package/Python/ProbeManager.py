#! /usr/bin/env python

import sys,json
import MySQLdb as mdb
from subprocess import Popen,PIPE
error=0
PATH_SCRIPT="Script"
HOST=Popen(PATH_SCRIPT+"/GetInfo.sh HOST", stdout=PIPE, shell=True).stdout.read()
DB=Popen(PATH_SCRIPT+"/GetInfo.sh DB", stdout=PIPE, shell=True).stdout.read()
PASSWORD=Popen(PATH_SCRIPT+"/GetInfo.sh PASS", stdout=PIPE, shell=True).stdout.read()
USER=Popen(PATH_SCRIPT+"/GetInfo.sh USER", stdout=PIPE, shell=True).stdout.read()

# Verification de la balise
# Boolean
def isBalise(capteurId):
	valid = False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT COUNT(*) FROM station where sta_id=\'%s\'" % capteurId)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid = True

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return valid

# Renvoie la listes des stations
# JSON [{"name":"name","longitude":"longitude","latitude":"latitude"}]
def stationList():
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT sta_name,sta_longitude,sta_latitude FROM station ")
			rows = cur.fetchall()
			myArray=[]
			for row in rows:
				tmp={"name":"name","longitude":"longitude","latitude":"latitude"}
				name=row[0]
				longitude=row[1]
				latitude=row[2]

				tmp["name"]=name
				tmp["longitude"]=longitude
				tmp["latitude"]=latitude
				myArray.append(tmp)

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return myArray

# Renvoie la listes des capteurs
# JSON {"capteur":[]}
def sensorList():
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT st_type FROM sensorType ")
			rows = cur.fetchall()
			myArray=[]
			for row in rows:
				myArray.append(row[0])
			tmp={"capteur":[]}
			tmp["capteur"]=myArray
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return tmp

# Renvoie la liste des stations avec les access pour un utilisateur
# JSON [{"name":"name"}]
def accessList(login):
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT sta.sta_name, sta.sta_longitude,sta.sta_latitude FROM station sta "+
						"INNER JOIN stationAccess staa ON staa.sta_id=sta.sta_id "+
						"INNER JOIN user u ON u.u_id=staa.u_id "+
						"INNER JOIN connection c ON u.u_id=c.u_id "+
						"where c.c_login=\'"+str(login)+"\'")
			rows = cur.fetchall()
			myArray=[]
			for row in rows:
				tmp={"name":"name","longitude":"longitude","latitude":"latitude"}
				name=row[0]
				longitude=row[0]
				latitude=row[0]

				tmp["name"]=name
				tmp["longitude"]=longitude
				tmp["latitude"]=latitude
				myArray.append(tmp)

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return myArray


# Met a jour les droits d'un utilisateur sur les stations
# Error Code
def userRights(login,liste):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Recuperation de l'id d'un utilisateur
			cur.execute("SELECT u_id FROM connection where c_login=\'"+str(login)+"\'")
			row= cur.fetchone()
			userId=row[0]
			access=accessList(login)
			station=stationList()
			myArray=[]

			# Mise en forme de la liste des station
			for tmpList in station:
				tmpJSON={"nom":"name","access":False}
				valid=False
				# Comparaison des listes
				for tmpAccess in access:
					if tmpList["name"]==tmpAccess["name"]:
						valid=True
						break
				tmpJSON["access"]=valid
				tmpJSON["nom"]=tmpList["name"]
				myArray.append(tmpJSON)
			originList=myArray

			# Compare liste pour decouvrir les changements
			for tmp in liste:
				for elem in originList:
					if tmp["nom"]==elem["nom"]:
						if tmp["access"]!=elem["access"]:
							# Recuperation de l'id de la station en cas de changement
							cur.execute("SELECT sta_id FROM station where sta_name=\'"+str(tmp["nom"])+"\'")
							row= cur.fetchone()
							stationId=row[0]
							# Mise a jour de la db
							if tmp["access"]== True:
								cur.execute("INSERT INTO stationAccess values (NULL,\'"+str(userId)+"\',\'"
											+str(stationId)+"\')")
							else:
								cur.execute("DELETE FROM stationAccess WHERE sta_id=\'"+str(stationId)
											+"\' AND u_id=\'"+str(userId)+"\'")


	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1000
	finally:
		con.close()
	return error


# Creation d'une station
# Error Code
def createStation(nom,longitude,latitude,date,capteur):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Creation de la station
			cur.execute("INSERT INTO station values (NULL,\'"+str(nom)+"\',\'"+str(longitude)+"\',\'"
						+str(latitude)+"\',\'"+str(date)+"\')")
			# Recuperation de l'id de la station
			cur.execute("SELECT sta_id FROM station where sta_name=\'"+str(nom)+"\' AND sta_longitude=\'"
						+str(longitude)+"\'AND sta_latitude=\'"+str(latitude)+"\'")
			sensorId=0
			rows = cur.fetchone()
			sensorId = rows[0]
			# Ajout de la liste des capteurs a la station
			for sensor in capteur:
				cur.execute("SELECT st_id FROM sensorType WHERE st_type=\'"+str(sensor)+"\'")
				rows = cur.fetchone()
				sensorType = rows[0]
				cur.execute("INSERT INTO sensor values (NULL,\'"+str(sensorType)+"\',\'"+str(sensorId)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1000
	finally:
		con.close()
	return error

# Creation d'un nouveau type de capteur
# Error Code
def createSensor(nom):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO sensorType values (NULL,\'"+str(nom)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1000
	finally:
		con.close()
	return error

# Modification d'un type de capteur pour une station
# Error Code
def modifSensorToStation(station,sensorType,modifType):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Recuperation de l'id correspondant au type
			cur.execute("SELECT st_id FROM sensorType WHERE st_type=\'"+sensorType+"\'")
			rows = cur.fetchone()
			sensorId = rows[0]
			# Recuperation de l'id de la station
			cur.execute("SELECT sta_id FROM station WHERE sta_name=\'"+station+"\'")
			rows = cur.fetchone()
			stationId = rows[0]
			if modifType == "delete":
				cur.execute("DELETE FROM sensor WHERE st_id=\'"+str(sensorId)+"\' AND sta_id=\'"+str(stationId)+"\'")
			elif modifType == "add":
				cur.execute("INSERT INTO sensor (s_id,st_id,sta_id) values (NULL,\'"+str(sensorId)+"\',\'"+str(stationId)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1000
	finally:
		con.close()
	return error

# Ajout d'un type de capteur a une station
# JSON {"capteur":[]}
def sensorOfStation(station):
	tmp={"capteur":[]}
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)

		with con:
			cur = con.cursor()
			# Recuperation de l'id de la station
			cur.execute("SELECT sta_id FROM station WHERE sta_name=\'"+station+"\'")
			rows = cur.fetchone()
			stationId = rows[0]

			# Recuperation des differents capteurs
			cur.execute("SELECT st.st_type FROM sensorType st "+
						"INNER JOIN sensor s ON st.st_id=s.st_id "+
						"where s.sta_id=\'"+str(stationId)+"\'")
			rows = cur.fetchall()
			myArray=[]
			for row in rows:
				myArray.append(row[0])
			tmp["capteur"]=myArray
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1000
	finally:
		con.close()
	return tmp


# Retourne les valeurs des capteurs d'une station entre 2 dates
# JSON [{"measure":"toto","value":"toto","date":"toto"}]
def capteurValue(login,capteurId,dateDebut,dateFin):
	myArray=[]
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Recuperation des mesures et dates pour chaque capteur
			cur.execute("SELECT m.m_value, st.st_type, m.m_date FROM measure m "+
						"INNER JOIN sensor s ON s.s_id=m.s_id "+
						"INNER JOIN sensorType st ON st.st_id=s.st_id "+
						"INNER JOIN station sta ON sta.sta_id=s.sta_id "+
						"INNER JOIN stationAccess staa ON staa.sta_id=sta.sta_id "+
						"INNER JOIN user u ON u.u_id=staa.u_id "+
						"INNER JOIN connection c ON u.u_id=c.u_id "+
						"where c.c_login=\'"+str(login)+"\' AND sta.sta_id=\'"+str(capteurId)+"\' "+
								"AND \'"+str(dateDebut)+"\'<= m.m_date AND \'"+str(dateFin)+"\'>= m.m_date")

			# Traitement et mises en forme des valeurs
			rows = cur.fetchall()
			for row in rows:
				tmp={"measure":"toto","value":"toto","date":"toto"}
				value=row[0]
				measure=row[1]
				date=row[2]

				tmp["value"]=float(str(value))
				tmp["measure"]=str(measure)
				tmp["date"]=float(date)
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
# JSON [{"mesure":"ozone","dateReleve":"toto"}]
def ozoneValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		if(dic["measure"]== "ozone"):
			tmp["mesure"]=dic["value"]
			tmp["dateReleve"]=dic["date"]
			retour.append(tmp)
	return retour

# Retourne les valeurs d'hygrometrie du capteur entre 2 dates
# JSON [{"mesure":"hygrometrie","dateReleve":"toto"}]
def hygrometrieValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		if(dic["measure"]== "hygrometrie"):
			tmp["mesure"]=dic["value"]
			tmp["dateReleve"]=dic["date"]
			retour.append(tmp)
	return retour

# Retourne les valeurs de temperature du capteur entre 2 dates
# JSON [{"mesure":"temperature","dateReleve":"toto"}]
def temperatureValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		if(dic["measure"]== "temperature"):
			tmp["mesure"]=dic["value"]
			tmp["dateReleve"]=dic["date"]
			retour.append(tmp)
	return retour

# Retourne les valeurs d'humidite du capteur entre 2 dates
# JSON [{"mesure":"humidite","dateReleve":"toto"}]
def humiditeValue(login,capteurId,dateDebut,dateFin):
	myArray=capteurValue(login,capteurId,dateDebut,dateFin)
	retour=[]
	for dic in myArray:
		tmp={"mesure":"toto","dateReleve":"toto"}
		if(dic["measure"]== "humidite"):
			tmp["mesure"]=dic["value"]
			tmp["dateReleve"]=dic["date"]
			retour.append(tmp)
	return retour
