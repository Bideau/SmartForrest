#! /usr/bin/env python
# I want to use : utf-8 please

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#* Import #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

import sys, json, os, string
import LoginManager as Login
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

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#* CORS #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
##	Empeche les erreurs de type CORS
#	@param resp
def addCorsHeaders(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'POST, GET, DELETE, PUT'
    resp.headers['Access-Control-Max-Age'] = '21600'
    resp.headers['Access-Control-Allow-Headers'] = 'accept, origin, authorization, content-type'

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*# Variable global #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*

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
def locations_GET():
	logger.info('/login		method : GET')
	logger.info(request)
	resp = make_response()
	addCorsHeaders(resp)
	try:

		req_data=[{'Valid':'True','Valid1':'True'}]
		#req_data=[{"display": "JavaScript Tutorial","url": "http://www.w3schools.com/js/default.asp"}]
		resp.headers['Content-Type'] = 'application/json'
		#si tu se passe bien retour d'un code erreur 200
		resp.status_code = 200
		resp.data = json.dumps(req_data)

	except:
		#si erreur retour d'un code erreur 500
	 	resp.status_code = 500
		resp.data = 'error 500 : Unexpected error'
		return resp
	logger.info(resp.data)
	return resp

@app.route('/login', methods=['POST'])
##	Permet de creer une nouvelle locations
def locations_POST():
	logger.info('/login		method : POST')
	logger.info(request.data)
	resp = make_response()
	addCorsHeaders(resp)
	#si aucune erreur alors le JSON est au bon format
	try:
		resp.headers['Content-Type'] = 'application/json'
		#recuperation de la donnee envoyer au serveur
		req_data = json.loads(request.data)
		logger.info(req_data)
		#recuperation du login
		login = str(req_data["login"])
		#recuperation du password
		password = str(req_data["password"])
		if( Login.isLogin(login) == True):
			# Si login et password valid 200
			if(Login.isPass(login,password) == True):
				resp.status_code = 200
			# Si password faux 400
			else:
				resp.status_code = 405
		# Si login faux 401
		else:
			resp.status_code = 403
		logger.info(req_data)

	except:
		#si une erreur de format retour erreur 400
		resp.status_code = 400
		resp.data = "error 400 : Bad format json"
		return

	return resp

#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*
#*#*#*#*#*#*#*#*#*#*#*#*#*#* Launch the server #*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#
#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*#*


app.run(host='0.0.0.0', port=8080, debug=True)