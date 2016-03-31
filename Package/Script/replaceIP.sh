#!/bin/bash
# Script pour mettre a jour les adresses ip du serveur Web
MY_PATH=$(pwd)
if [[ -d $MY_PATH/Script ]] ; then
	MY_PATH=$MY_PATH/Script
fi
WEBPATH=$($MY_PATH/GetInfo.sh WEBPATH)
INTERFACE=$($MY_PATH/GetInfo.sh INTERFACE)
PORT=8080
serverIP=$(ip addr | grep inet | grep "$INTERFACE" | awk -F" " '{print $2}'| sed -e 's/\/.*$//')
sed -i -e s"|var adresseIPServeur = .*;|var adresseIPServeur = \"http://$serverIP:$PORT/\" ;|"g $WEBPATH/assets/js/MyJs.js
sed -i -e s"|var adresseIPServeur = .*;|var adresseIPServeur = \"http://$serverIP:$PORT/\" ;|"g $WEBPATH/assets/js/FullScreenGraph.js
