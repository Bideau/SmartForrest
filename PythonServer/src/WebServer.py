#! /usr/bin/env python
# I want to use : utf-8 please

# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#* Import #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

import sys, json, os, string, thread
import LoginManager as Login
import ProbeManager as Probe
from flask import *

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)

################################################################################
################################### LOGGER #####################################
################################################################################

import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
if not os.path.isdir('log'):
	os.mkdir('log')

# create formatter for the type of log
formatter = logging.Formatter('%(asctime)s :: %(levelname)s :: %(message)s')
# file handler, filename = server.log, 1Mo max, 5 log (4  archived and actual log)
file_handler = RotatingFileHandler('log/server.log', 'a', 1000000, 5)

# level INFO with the previous formatter
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# one handler for write DEBUG in the console
steam_handler = logging.StreamHandler()
steam_handler.setLevel(logging.DEBUG)
logger.addHandler(steam_handler)

logger.info('******************** NEW SESSION ********************')
logger.info('Logger is ready')


# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#* CORS #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
##	Empeche les erreurs de type CORS
#	@param resp
def addCorsHeaders(resp):
	resp.headers['Access-Control-Allow-Origin'] = '*'
	resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT'
	resp.headers['Access-Control-Max-Age'] = '21600'
	resp.headers['Access-Control-Allow-Headers'] = 'accept, origin, authorization, content-type'


# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*# Variable global #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

#################################### / #########################################
## root et redirection

@app.route('/')
##	acces a la racine du service web
def root():
	resp = make_response()
	resp.status_code = 200
	resp.data = 'Root, nothing to see here'
	return resp

@app.route('/')
## Redirige sur la page /static/main.html
def redirectToMain():
	return redirect('/static/main.html')

@app.route('/login', methods=['POST'])
##	Permet la connexion du login
## Resp {"nom":"toto","prenom":"toto","description":"toto","login":"login"}
def login_POST():
	logger.info('\n/login		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	tmp={"nom":"toto","prenom":"toto","description":"toto","login":"toto"}
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du password
		password = str(req_data["password"])
		# Test des informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			# Si login et password valid 200
			if (Login.isPass(login, password) == True):
				resp.status_code = 200
				tmp=Login.userInfo(login)
			# Si password faux 1003
			else:
				resp.status_code = 1003
		# Si login faux 1002
		else:
			resp.status_code = 1002
		# Conversion Reponse to JSON
		resp.data=json.dumps(tmp)
		logger.info(resp.data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp

	return resp


@app.route('/user', methods=['POST'])
##	Permet de creer un nouveau user
## Resp No Resp
def user_POST():
	logger.info('\n/user		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du password
		password = str(req_data["password"])
		# recuperation du nom
		nom = str(req_data["nom"])
		# recuperation du prenom
		prenom = str(req_data["prenom"])
		# recuperation du mail
		mail = str(req_data["mail"])
		# recuperation du description
		desc = str(req_data["description"])
		# Test des informations de connexion de l'utilisateur
		if (Login.isLogin(login) == False):
			resp.status_code = Login.insertUser(login, password, nom, prenom, desc,mail)
		# Si login existe deja 1005
		else:
			resp.status_code = 1005

	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/deletedUser', methods=['POST'])
##	Permet de supprimer un nouveau user
## Resp No Resp
def deletedUser_POST():
	logger.info('\n/deletedUser		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# Test des informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			resp.status_code = Login.userSuppr(login)
		# Si login existe deja 1002
		else:
			resp.status_code = 1002
		#logger.info(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/userList', methods=['GET'])
##	Retourne tous les users
## Resp [{"nom":"toto","prenom":"toto","login":"toto"}]
def userlist_GET():
	logger.info('\n/userList		method : GET')
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data=Login.userList()
		resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/ModifyDescription', methods=['POST'])
##	Modifie la description d'un utilisateur
## Resp No Resp
def ModifyDescription_POST():
	logger.info('\n/ModifyDescription		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation de la description
		desc = str(req_data["description"])
		# recuperation de la description
		mail = str(req_data["mail"])
		req_data=Login.descModif(login,desc)
		if req_data == 200 :
			req_data=Login.mailModif(login,mail)
		resp.status_code=req_data
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/userRights', methods=['POST'])
##	Changement des droits d'un utilisateur sur les stations
## Resp No Resp
def userRights_POST():
	logger.info('\n/userRights		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation de la liste des droits
		liste = req_data["liste"]
		resp.status_code=Probe.userRights(login,liste)

	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/modifyPassword', methods=['POST'])
##	Changement du mot de passe d'un utilisateur
## Resp No Resp
def modifyPassword_POST():
	logger.info('\n/modifyPassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du ancienPassword
		aPassword = str(req_data["ancienPassword"])
		# recuperation du newPassword
		nPassword = str(req_data["newPassword"])
		# Test les informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			# Si login et password valid 200
			if (Login.isPass(login, aPassword) == True):
				resp.status_code=Login.changePass(login,nPassword)
			# Si password faux 1003
			else:
				resp.status_code = 1003
		# Si login faux 1002
		else:
			resp.status_code = 1002
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/forgotPassword', methods=['POST'])
##	Envoie de mail et creation de mot de passe en cas d'oublis du mot de passe
## Resp No Resp
def forgotPassword_POST():
	logger.info('\n/forgotPassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du mail
		mail = str(req_data["mail"])
		# Test les informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			# Si login et password valid 200
			resp.status_code=Login.forgetPassword(login,mail)
		# Si login faux 1002
		else:
			resp.status_code = 1002
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/erasePassword', methods=['POST'])
##	Changement du mot de passe temporaire d'un utilisateur
## Resp No Resp
def erasePassword_POST():
	logger.info('\n/erasePassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du password
		password = str(req_data["password"])
		# Test les informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			# Si login et password valid 200
			resp.status_code=Login.changePass(login,password)
		# Si login faux 1002
		else:
			resp.status_code = 1002
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/capteur', methods=['POST'])
##	Permet de creer un nouveau capteur
## Resp [{"mesure":"ozone","dateReleve":"toto"}]
def capteur_POST():
	logger.info('\n/capteur		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		result={}
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du capteurId
		capteurId = str(req_data["capteurId"])
		# recuperation de la valeur a renvoyer
		mesure = str(req_data["mesure"])
		# recuperation du dateDebut
		dateDebut = req_data["dateDebut"]
		# recuperation du dateFin
		dateFin = req_data["dateFin"]
		myArray=[]
		# Test les informations de connexion de l'utilisateur
		if (Login.isLogin(login) == True):
			if ( Probe.isBalise(capteurId)==True):
				if(Login.userAccess(login,capteurId)==True):
					if(mesure == "temperature"):
						myArray=Probe.temperatureValue(login,capteurId,dateDebut,dateFin)
					elif(mesure == "ozone"):
						myArray=Probe.ozoneValue(login,capteurId,dateDebut,dateFin)
					elif(mesure == "hygrometrie"):
						myArray=Probe.hygrometrieValue(login,capteurId,dateDebut,dateFin)
					elif(mesure == "humidite"):
						myArray=Probe.humiditeValue(login,capteurId,dateDebut,dateFin)
					else:
						myArray=Probe.capteurValue(login,capteurId,dateDebut,dateFin)

					result["releve"]=myArray
					resp.data=json.dumps(result)
					resp.status_code = 200
					logger.info(resp.data)
				else:
					# Le user n'a pas acces au capteur
					resp.status_code=1007
			else:
				# Le capteur n'existe pas
				resp.status_code=1006
		else:
			# Le login n'existe pas
			resp.status_code=1002
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/stationList', methods=['GET'])
##	Retourne tous les stations
## Resp [{"name":"name","longitude":"longitude","latitude":"latitude"}]
def probeList_GET():
	logger.info('\n/stationList		method : GET')
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data=Probe.stationList()
		resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/sensorList', methods=['GET'])
##	Retourne tous les sondes
## Resp {"capteur":[]}
def sensorList_GET():
	logger.info('\n/sensorList		method : GET')
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data=Probe.sensorList()
		resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/addStation', methods=['POST'])
##	Ajout d'une station
## Resp No Resp
def addStation_POST():
	logger.info('\n/addStation		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du nom
		nom = str(req_data["nom"])
		# recuperation de la longitude
		longitude = str(req_data["longitude"])
		# recuperation de la latitude
		latitude = str(req_data["latitude"])
		# recuperation de la date
		date =req_data["dateDeploiement"]
		# recuperation des capteurs
		capteur = req_data["capteurs"]
		resp.status_code=Probe.createStation(nom,longitude,latitude,date,capteur)
		#resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/addSensor', methods=['POST'])
##	Aout d'un type de capteur
## Resp No Resp
def addSensor_POST():
	logger.info('\n/addSensor		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du nom
		nom = str(req_data["nom"])

		resp.status_code=Probe.createSensor(nom)
		#resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info(resp.data)
	return resp

@app.route('/accessList', methods=['POST'])
##	Renvoie la liste des accees d'un utilisateur
## Resp {"liste":[{"nom":"nom","access":True}]}
def accessList_POST():
	logger.info('\n/accessList		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du login
		login = str(req_data["login"])
		access=Probe.accessList(login)
		list=Probe.stationList()
		myArray=[]

		# Croise les informations des listes pour crees un JSON des accees
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
		req_data={"liste":[]}
		req_data["liste"]=myArray
		resp.data = json.dumps(req_data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	logger.info("Response")
	logger.info(resp.data)
	return resp

@app.route('/addSensorToStation', methods=['POST'])
##	Ajout d'un capteur a une station
## Resp No Resp
def addSensorToStation_POST():
	logger.info('\n/addSensorToStation		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du nom de la station
		station = str(req_data["station"])
		# recuperation du type de capteur a ajouter a la station
		sensorType = req_data["capteurType"]
		resp.status_code=Probe.modifSensorToStation(station,sensorType,"add")
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/deletedSensorToStation', methods=['POST'])
##	Ajout d'un capteur a une station
## Resp No Resp
def deletedSensorToStation_POST():
	logger.info('\n/deletedSensorToStation		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du nom de la station
		station = str(req_data["station"])
		# recuperation du type de capteur a ajouter a la station
		sensorType = req_data["capteurType"]
		resp.status_code=Probe.modifSensorToStation(station,sensorType,"delete")
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/sensorOfStation', methods=['POST'])
##	Recuperation des capteurs d'une station
## Resp {"capteur":[]}
def sensorOfStation_POST():
	logger.info('\n/sensorOfStation		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		resp.status_code = 200
		req_data = json.loads(request.data)
		# recuperation du nom de la station
		station = str(req_data["nom"])
		tmp=Probe.sensorOfStation(station)
		resp.data=json.dumps(tmp)
		logger.info(resp.data)
	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp


# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#* Launch the server #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

app.run(host='172.30.0.103', port=8080, debug=False)

