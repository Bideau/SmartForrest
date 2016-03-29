#!/bin/bash
# Fonction de recuperation des informations de la base de donnees
# Prend en parametre l'information voulant etre recuperee
# Peut etre mise en place de la prise en parametre du chemin du fichier config

PATH_SCRIPT=$(pwd)
if [[ -d $PATH_SCRIPT/Script ]] ; then
	PATH_SCRIPT=$PATH_SCRIPT/Script
fi
function GetHost {
	HOST=$(cat $PATH_SCRIPT/../config.ini | grep "HOST" | sed -e s'/HOST=//'g  -e s/\'//g)
	echo $HOST
}
function GetDB {
	DB=$(cat $PATH_SCRIPT/../config.ini | grep "DB" | sed -e s'/DB=//'g -e s/\'//g)
	echo $DB
}
function GetPass {
	PASS=$(cat $PATH_SCRIPT/../config.ini | grep "PASSWORD" | sed -e s'/PASSWORD=//'g -e s/\'//g)
	echo $PASS
}
function GetUser {
	USER=$(cat $PATH_SCRIPT/../config.ini | grep "USER" | sed -e s'/USER=//'g -e s/\'//g)
	echo $USER
}
function GetWebPath {
	WEBPATH=$(cat $PATH_SCRIPT/../config.ini | grep "WEBPATH" | sed -e s'/WEBPATH=//'g -e s/\'//g)
	echo $WEBPATH
}
function GetInterface {
	INTERFACE=$(cat $PATH_SCRIPT/../config.ini | grep "INTERFACE" | sed -e s'/INTERFACE=//'g -e s/\'//g)
	echo $INTERFACE
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
	("WEBPATH")
		VALUE=$(GetWebPath)
	;;
	("INTERFACE")
		VALUE=$(GetInterface)
	;;
esac
echo -n "$VALUE" 
