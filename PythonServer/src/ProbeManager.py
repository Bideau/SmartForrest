#! /usr/bin/env python

import sys,json
import MySQLdb as mdb
error=0
HOST='srvmysql.imerir.com'
DB='SmartForest'
PASSWORD='LjcX7vWRMs84jJ3h'
USER='SmartForest'

# Verification du login
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
	print(valid)
	return valid

# Renvoie la listes des stations
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
def accessList(login):
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT sta.sta_name FROM station sta "+
						"INNER JOIN stationAccess staa ON staa.sta_id=sta.sta_id "+
						"INNER JOIN user u ON u.u_id=staa.u_id "+
						"INNER JOIN connection c ON u.u_id=c.u_id "+
						"where c.c_login=\'"+str(login)+"\'")
			rows = cur.fetchall()
			myArray=[]
			for row in rows:
				tmp={"name":"name"}
				name=row[0]

				tmp["name"]=name
				myArray.append(tmp)

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return myArray


# Renvoie la liste des stations avec les access pour un utilisateur
def userRights(login,liste):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT u_id FROM connection where c_login=\'"+str(login)+"\'")
			row= cur.fetchone()
			userId=row[0]
			access=accessList(login)
			list=stationList()
			myArray=[]

			for tmpList in list:
				tmpJSON={"nom":"name","access":False}
				valid=False
				for tmpAccess in access:
					if tmpList["name"]==tmpAccess["name"]:
						valid=True
						break
				tmpJSON["access"]=valid
				tmpJSON["nom"]=tmpList["name"]
				myArray.append(tmpJSON)
			originList=myArray

			# Compare liste
			for tmp in liste:
				for elem in originList:
					if tmp["nom"]==elem["nom"]:
						print("toto1")
						if tmp["access"]!=elem["access"]:
							print("toto2")
							cur.execute("SELECT sta_id FROM station where sta_name=\'"+str(tmp["nom"])+"\'")
							row= cur.fetchone()
							stationId=row[0]
							if tmp["access"]== True:
								print("Insert")
								cur.execute("INSERT INTO stationAccess values (NULL,\'"+str(userId)+"\',\'"
											+str(stationId)+"\')")
							else:
								cur.execute("DELETE FROM stationAccess WHERE sta_id=\'"+str(stationId)
											+"\' AND u_id=\'"+str(userId)+"\'")


	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return error


# Creation de balise
def createStation(nom,longitude,latitude,date,capteur):
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO station values (NULL,\'"+str(nom)+"\',\'"+str(longitude)+"\',\'"
						+str(latitude)+"\',\'"+str(date)+"\')")
			cur.execute("SELECT sta_id FROM station where sta_name=\'"+str(nom)+"\' AND sta_longitude=\'"
						+str(longitude)+"\'AND sta_latitude=\'"+str(latitude)+"\'")
			sensorId=0
			rows = cur.fetchone()
			sensorId = rows[0]
			for sensor in capteur:
				cur.execute("SELECT st_id FROM sensorType WHERE st_type=\'"+str(sensor)+"\'")
				rows = cur.fetchone()
				sensorType = rows[0]
				cur.execute("INSERT INTO sensor values (NULL,\'"+str(sensorType)+"\',\'"+str(sensorId)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return 200

# Creation de balise
def createSensor(nom):
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("INSERT INTO sensorType values (NULL,\'"+str(nom)+"\')")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		sys.exit(1)
	finally:
		con.close()
	return 200


# Retourne les valeurs des capteurs d'une balise entre 2 dates
def capteurValue(login,capteurId,dateDebut,dateFin):
	myArray=[]
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT m.m_value, st.st_type, m.m_date FROM measure m "+
						"INNER JOIN sensor s ON s.s_id=m.s_id "+
						"INNER JOIN sensorType st ON st.st_id=s.st_id "+
						"INNER JOIN station sta ON sta.sta_id=s.sta_id "+
						"INNER JOIN stationAccess staa ON staa.sta_id=sta.sta_id "+
						"INNER JOIN user u ON u.u_id=staa.u_id "+
						"INNER JOIN connection c ON u.u_id=c.u_id "+
						"where c.c_login=\'"+str(login)+"\' AND sta.sta_id=\'"+str(capteurId)+"\' "+
								"AND \'"+str(dateDebut)+"\'<= m.m_date AND \'"+str(dateFin)+"\'>= m.m_date")

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