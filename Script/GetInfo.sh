#!/bin/bash
# Fonction de recuperation des informations de la base de donnees
# Prend en parametre l'information voulant etre recuperee
# Peut etre mise en place de la prise en parametre du chemin du fichier config
function GetHost {
	HOST=$(cat configMySQL.ini | grep "HOST" | sed -e s'/HOST=//'g  -e s/\'//g)
	echo $HOST
}
function GetDB {
	DB=$(cat configMySQL.ini | grep "DB" | sed -e s'/DB=//'g -e s/\'//g)
	echo $DB
}
function GetPass {
	PASS=$(cat configMySQL.ini | grep "PASSWORD" | sed -e s'/PASSWORD=//'g -e s/\'//g)
	echo $PASS
}
function GetUser {
	USER=$(cat configMySQL.ini | grep "USER" | sed -e s'/USER=//'g -e s/\'//g)
	echo $USER
}

ARG=$1 
case $ARG in 
	("USER")
		VALUE=$(GetUser)
	;;
	("PASS")
		VALUE=$(GetPass)
	;;
	("DB")
		VALUE=$(GetDB)
	;;
	("HOST")
		VALUE=$(GetHost)
	;;
esac
echo -n "$VALUE" 
