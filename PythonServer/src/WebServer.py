#! /usr/bin/env python
# I want to use : utf-8 please

# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#* Import #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

import sys, json, os, string, thread
import LoginManager as Login
from flask import *

import ServerSocket

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
##	Retourne toutes les locations
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
		resp.data=json.dumps(tmp)
		logger.info(resp.data)
	except:
		# si une erreur de format retour erreur 1004
		resp.status_code = 1004
		resp.data = "error 1004 : Bad format json"
		return resp

	return resp


#
# {
# "login": "toto",
# "password": "tata",
# "nom": "Doe",
# "prenom": "John",
# "description": "Description Test IT"
# }
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
		logger.info("login " + login)
		# recuperation du password
		password = str(req_data["password"])
		logger.info("password " + password)
		# recuperation du nom
		nom = str(req_data["nom"])
		logger.info("nom " + nom)
		# recuperation du prenom
		prenom = str(req_data["prenom"])
		logger.info("prenom " + prenom)
		# recuperation du description
		desc = str(req_data["description"])
		logger.info("Desc " + desc)
		if (Login.isLogin(login) == False):
			resp.status_code = Login.insertUser(login, password, nom, prenom, desc)
		# Si login existe deja 1005
		else:
			resp.status_code = 1005
		logger.info(req_data)

	except:
		# si une erreur de format retour erreur 1003
		resp.status_code = 1003
		resp.data = "error 400 : Bad format json"
		return resp
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
			if ( Login.isBalise(capteurId)==True):
				if(Login.userAccess(login,capteurId)==True):
					if(mesure == "temperature"):
						myArray=Login.temperatureValue(login,capteurId,dateDebut,dateFin)
					elif(mesure == "ozone"):
						myArray=Login.ozoneValue(login,capteurId,dateDebut,dateFin)
						print(myArray)
					elif(mesure == "hygrometrie"):
						myArray=Login.hygrometrieValue(login,capteurId,dateDebut,dateFin)
					elif(mesure == "humidite"):
						myArray=Login.humiditeValue(login,capteurId,dateDebut,dateFin)
					else:
						myArray=Login.capteurValue(login,capteurId,dateDebut,dateFin)

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


# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
# *#*#*#*#*#*#*#*#*#*#*#*#*#* Launch the server #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
# *#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
try:
	thread.start_new_thread( ServerSocket.socketServer, ("Thread-2",'172.30.0.103',8081,) )
	thread.start_new_thread( app.run(host='172.30.0.103', port=8080, debug=False), ("Thread-1", ) )
except:
	print ("Error: unable to start thread")
#thread.start_new_thread( ServerSocket.socketServer, ("Thread-2",'127.0.0.1',8083,) )
#app.run(host='172.30.0.103', port=8080, debug=False)

