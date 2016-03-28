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

"""
CRITICAL	50
ERROR		40
WARNING		30
INFO		20		<-- file lvl
DEBUG		10		<-- Global level / Console lvl
"""

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


@app.route('/login', methods=['GET'])
##	Retourne les login
def login_GET():
	logger.info('/login		method : GET')
	logger.info(request)
	resp = make_response()
	addCorsHeaders(resp)
	try:

		req_data = [{'Valid': 'True', 'Valid1': 'True'}]
		# req_data=[{"display": "JavaScript Tutorial","url": "http://www.w3schools.com/js/default.asp"}]
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		resp.data = json.dumps(req_data)

	except:
		# si erreur retour d'un code erreur 1000
		resp.status_code = 1000
		resp.data = "error 1000 : Unexpected error"
		return resp
	logger.info(resp.data)
	return resp


@app.route('/login', methods=['POST'])
##	Permet de connexion login
def login_POST():
	logger.info('/login		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	tmp={"nom":"toto","prenom":"toto","description":"toto","login":"toto"}
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du password
		password = str(req_data["password"])
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
def user_POST():
	logger.info('/user		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		logger.info(req_data)
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
		if (Login.isLogin(login) == False):
			resp.status_code = Login.insertUser(login, password, nom, prenom, desc,mail)
		# Si login existe deja 1005
		else:
			resp.status_code = 1005
		logger.info(req_data)

	except Exception as e:
		print (e)
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp
	return resp

@app.route('/deletedUser', methods=['POST'])
##	Permet de supprimer un nouveau user
def deletedUser_POST():
	logger.info('/deletedUser		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		logger.info("REQ_DATA "+str(req_data))
		# recuperation du login
		login = str(req_data["login"])
		logger.info(login)
		if (Login.isLogin(login) == True):
			resp.status_code = Login.userSuppr(login)
			logger.info("toto")
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
def userlist_GET():
	logger.info('/userList		method : GET')
	logger.info(request)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
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
def ModifyDescription_POST():
	logger.info('/ModifyDescription		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation de la description
		desc = str(req_data["description"])
		# recuperation de la description
		mail = str(req_data["mail"])
		req_data=Login.descModif(login,desc)
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

@app.route('/capteur', methods=['POST'])
##	Permet de creer un nouveau capteur
def capteur_POST():
	logger.info('/capteur		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	# si aucune erreur alors le JSON est au bon format
	try:
		result={}
		resp.headers['Content-Type'] = 'application/json'
		# recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		logger.info(req_data)
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

					#result={"releve":myArray}
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
##	Retourne tous les sondes
def probeList_GET():
	logger.info('/stationList		method : GET')
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
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
def sensorList_GET():
	logger.info('/sensorList		method : GET')
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
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
def addStation_POST():
	logger.info('/addStation		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
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
##	Ajout d'une station
def addSensor_POST():
	logger.info('/addSensor		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
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
##	Ajout d'une station
def accessList_POST():
	logger.info('/accessList		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		access=Probe.accessList(login)
		list=Probe.stationList()
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

@app.route('/userRights', methods=['POST'])
##	Ajout d'une station
def userRights_POST():
	logger.info('/userRights		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
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
##	Ajout d'une station
def modifyPassword_POST():
	logger.info('/modifyPassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du ancienPassword
		aPassword = str(req_data["ancienPassword"])
		# recuperation du newPassword
		nPassword = str(req_data["newPassword"])
		if (Login.isLogin(login) == True):
			# Si login et password valid 200
			if (Login.isPass(login, aPassword) == True):
				resp.status_code = 200
				tmp=Login.changePass(login,nPassword)
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
##	Ajout d'une station
def forgotPassword_POST():
	logger.info('/forgotPassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du mail
		mail = str(req_data["mail"])
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
##	Ajout d'une station
def erasePassword_POST():
	logger.info('/erasePassword		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	try:
		resp.headers['Content-Type'] = 'application/json'
		# si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		req_data = json.loads(request.data)
		logger.info(req_data)
		# recuperation du login
		login = str(req_data["login"])
		# recuperation du password
		password = str(req_data["password"])
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


# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#* Launch the server #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#try:
#	thread.start_new_thread( ServerSocket.socketServer, ("Thread-2",'172.30.0.103',8081,) )
#	thread.start_new_thread( app.run(host='172.30.0.103', port=8080, debug=False), ("Thread-1", ) )
#except:
#	print ("Error: unable to start thread")
#thread.start_new_thread( ServerSocket.socketServer, ("Thread-2",'127.0.0.1',8083,) )
app.run(host='172.30.0.103', port=8080, debug=False)

