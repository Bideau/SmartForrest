#!/bin/bash
# Script d'envoie des donnees vers le serveur
# Compress les fichiers JSON puis les envois avec rsync
# Communication crypter avec une cle ssh
# Ne prend pas de parametre

date
SERVER=172.20.8.19
HOSTNAME=gbideau
DIR_DEST=/imerir/eleves/gbideau/data/
DIR_SCRIPT=/imerir/eleves/gbideau/Script
DIR_DATA=~/data
DIR_ARCH=~/tmp
timestamp=$(date +%F-%H-%M)

echo "Compressing Phase"
cd $DIR_DATA
tar -c --xz -f $DIR_ARCH/data_$timestamp.tar.xz ./* && xz -t $DIR_ARCH/data_$timestamp.tar.xz

echo "Sending Phase"
rsync -v  $DIR_ARCH/* $HOSTNAME@$SERVER:$DIR_DEST && rm -f $DIR_ARCH/*
ssh $HOSTNAME@$SERVER bash $DIR_SCRIPT/uptoDB.sh data_$timestamp.tar.xz 
date
