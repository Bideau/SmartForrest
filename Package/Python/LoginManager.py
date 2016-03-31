#! /usr/bin/env python

import MySQLdb as mdb
import smtplib
import string
from random import sample, choice
from subprocess import Popen,PIPE
import md5

error=0
PATH_SCRIPT="Script"
HOST=Popen(PATH_SCRIPT+"/GetInfo.sh HOST", stdout=PIPE, shell=True).stdout.read()
DB=Popen(PATH_SCRIPT+"/GetInfo.sh DB", stdout=PIPE, shell=True).stdout.read()
PASSWORD=Popen(PATH_SCRIPT+"/GetInfo.sh PASS", stdout=PIPE, shell=True).stdout.read()
USER=Popen(PATH_SCRIPT+"/GetInfo.sh USER", stdout=PIPE, shell=True).stdout.read()

# Generation mot de passe
# Mot de passe aleatoire
def genPass(length):
	chars = string.letters + string.digits
	retour=''.join(choice(chars) for _ in range(length))
	return retour

# Verification du login
# Boolean
def isLogin(login):
	valid = False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT COUNT(*) FROM connection where c_login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid = True

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error= 1001

	finally:
		con.close()
	return valid

# Verification du mot de passe
# Boolean
def isPass(login, password):
	valid=False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT c_password, c_adminKey FROM connection where c_login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == password):
					valid=True
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error= 1001

	finally:
		con.close()
	return valid

# Verification acces admin
# Boolean
def isAdmin(login):
	valid=False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT c_adminKey FROM connection where c_login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid=True
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		return 1001
	finally:
		con.close()
	return valid

#Verification mot de passe temporaire
# Boolean
def isTemp(login):
	valid=False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Recuperation de si le mot de passe est temporaire
			cur.execute("SELECT c_tempPassword FROM connection where c_login=\'%s\'" % login)
			rows = cur.fetchall()
			for row in rows:
				if (row[0] == 1):
					valid=True

			# Desactivation du mot de passe temporaire
			if(valid==True):
				newPass=md5.new(genPass(12)).hexdigest()
				cur.execute("UPDATE connection SET c_password=\'"+str(newPass)+"\',c_tempPassword=0 where c_login=\'"
							+str(login)+"\'")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		return 1001
	finally:
		con.close()
	return valid

# Changement du mot de passe
# Error Code
def changePass(login,newPassword):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("UPDATE connection SET c_password=\'"+newPassword+"\' where c_login=\'"+login+"\'")

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error= 1001

	finally:
		con.close()
	return error

# Insert un utilisateur et un login dans la BDD
# Error Code
def insertUser(login, password, nom, prenom, desc,mail):
	UserId=0
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			# Insertion des informations utilisateur
			cur.execute("INSERT INTO user (u_id,u_lastName,u_firstName,u_description,u_mail) values (NULL,\'"
						+nom+"\',\'"+prenom+"\',\'"+desc+"\',\'"+mail+"\')")
			# Recuperation de l'id utilisateur
			cur.execute("SELECT u_id FROM user where u_lastName=\'"+nom+"\' AND u_firstName=\'"
						+prenom+"\' AND u_description=\'"+desc+"\' AND u_mail=\'"+mail+"\'")
			UserId=0
			rows = cur.fetchall()
			for row in rows:
				UserId = row[0]
			# Insertion des informations de connexion
			cur.execute("INSERT INTO connection (c_id,u_id,c_login,c_password,c_adminKey,c_tempPassword)"+
						" values (NULL,\'"+str(UserId)+"\',\'"+login+"\',\'"+password+"\',False,False)")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error= 1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error= 1000
	finally:
		con.close()
	return error

# Retourne les information de l'utilisateur du login
# JSON {"nom":"toto","prenom":"toto","description":"toto","login":"login"}
def userInfo(login):
	tmp={"nom":"toto","prenom":"toto","description":"toto","login":login}
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT u.u_lastName,u.u_firstName,u.u_description,u.u_mail FROM connection c INNER JOIN user u "+
						"ON u.u_id=c.u_id where c.c_login=\'"+str(login)+"\' ")
			rows = cur.fetchone()
			# Recuperation des donnees
			nom=rows[0]
			prenom=rows[1]
			desc=rows[2]
			mail=rows[3]

			tmp["nom"]=nom
			tmp["prenom"]=prenom
			tmp["description"]=desc
			tmp["isAdmin"]=isAdmin(login)
			tmp["motDePasseUnique"]=isTemp(login)
			tmp["mail"]=mail
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

# Suppression d'un login
# Error Code
def userSuppr(login):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("DELETE FROM connection where c_login=\'"+str(login)+"\' ")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return error

# Modification de la description d'un utilisateur
# Error Code
def descModif(login,desc):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("UPDATE user u,connection c SET u.u_description=\'"+str(desc)+"\' where c.c_login=\'"+str(login)+"\' AND u.u_id=c.u_id ")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return error

# Modification d'un mail d'un utilisateur
# Error Code
def mailModif(login,mail):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("UPDATE user u,connection c SET u.u_mail=\'"+str(mail)+"\' where c.c_login=\'"+str(login)+"\' AND u.u_id=c.u_id")
	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return error

# Retourne si l'utilisateur a les droits pour le capteur
# Boolean
def userAccess(login,capteurId):
	valid=False
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT Count(sta.sta_id) FROM station sta "+
						"INNER JOIN stationAccess staa ON staa.sta_id=sta.sta_id "+
						"INNER JOIN user u ON u.u_id=staa.u_id "+
						"INNER JOIN connection c ON u.u_id=c.u_id "+
						"where c.c_login=\'"+str(login)+"\' AND sta.sta_id=\'"+str(capteurId)+"\' ")
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

# Retourne la  liste des utilisateur
# JSON [{"nom":"toto","prenom":"toto","login":"toto"}]
def userList():
	myArray=[]
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			cur = con.cursor()
			cur.execute("SELECT u.u_lastName,u.u_firstName,c.c_login FROM connection c INNER JOIN user u "+
						"ON u.u_id=c.u_id")

			rows = cur.fetchall()
			for row in rows:
				tmp={"nom":"toto","prenom":"toto","login":"toto"}
				nom=row[0]
				prenom=row[1]
				login=row[2]

				tmp["nom"]=nom
				tmp["prenom"]=prenom
				tmp["login"]=login
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

# Envoie de mail avec mot de passe temporaire
# Error Code
def forgetPassword(login,mail):
	error=200
	try:
		con = mdb.connect(HOST, USER, PASSWORD, DB)
		with con:
			userId=0
			tmpMail=""
			sender="smartforest66@gmail.com"
			password='Smart66Forest'
			cur = con.cursor()
			# Recuperation mail utilisateur
			cur.execute("SELECT u.u_mail,u.u_id FROM connection c INNER JOIN user u "+
						"ON u.u_id=c.u_id WHERE c.c_login=\'"+str(login)+"\'")

			rows = cur.fetchall()
			for row in rows:
				tmpMail=row[0]
				userId=row[1]
			# Test du mail utilisateur
			if tmpMail == mail:
				# Generation du mot de passe temporaire
				tmpPass=genPass(10)
				# Envoie du mail
				headers = "From: <"+sender+">\n"+"To: <"+mail+">\n"+"Subject: Changement de mot passe\n"+\
						  "\nVotre nouveau mot de passe temporaire est : " + tmpPass + " \n"

				# Mise a jour de la base de donnees aves le nouveau mot de passe
				newPass=md5.new(tmpPass).hexdigest()
				cur.execute("UPDATE connection SET c_password=\'"+str(newPass)+"\',c_tempPassword=1 where c_login=\'"
							+str(login)+"\' AND u_id=\'"+str(userId)+"\'")
				server = smtplib.SMTP('smtp.gmail.com:587')
				server.ehlo()
				server.starttls()
				server.login(sender,password)
				server.sendmail(sender, mail, headers)
				server.quit()

	except mdb.Error as e:
		print("Error %d: %s") % (e.args[0], e.args[1])
		error=1001
	except Exception as e:
		# si une erreur de format retour erreur 1000
		print(e)
		error=1000
	finally:
		con.close()
	return error

