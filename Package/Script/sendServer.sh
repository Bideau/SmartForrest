#!/bin/bash
# Script d'envoie des donnees vers le serveur
# Compress les fichiers JSON puis les envois avec rsync
# Communication crypter avec une cle ssh
# Peut prendre en parametre les conf serveur et hostname
# -s serverIp
# -h hostname

date
ARGS=$1
SERVER=192.168.1.104
HOSTNAME=smartforest

DIR_DEST=/home/smartforest/data/
DIR_SCRIPT=/home/smartforest/Script
DIR_DATA=~/Rapberry/server/data
DIR_ARCH=~/Raspberry/server/tmp

timestamp=$(date +%F-%H-%M)

ArgServer=false
ArgHost=false

for i in $ARGS ; do
	case $i in
		(-s)
			ArgServer=true
			ArgHost=false
		;;
		(-h)
			ArgServer=true
			ArgHost=false
		;;
		(*)
			if [[ $ArgServer == true ]] ; then
				SERVER=$i
			elif [[ $ArgHost == true ]] ; then
				HOSTNAME=$i
			fi
		;;
	esac
done

echo "Compressing Phase"
cd $DIR_DATA
mkdir $DIR_ARCH
tar -c --xz -f $DIR_ARCH/data_$timestamp.tar.xz ./* && xz -t $DIR_ARCH/data_$timestamp.tar.xz

echo "Sending Phase"
rsync -v  $DIR_ARCH/* $HOSTNAME@$SERVER:$DIR_DEST && rm -f $DIR_ARCH/*
ssh $HOSTNAME@$SERVER bash $DIR_SCRIPT/uptoDB.sh data_$timestamp.tar.xz 
rm -fr $DIR_ARCH
rm -fr $DIR_DATA/*
date
