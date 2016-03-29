#!/bin/bash
# Sript permettant l'enregistrement des donnees provenant du Raspberry
# Besoin du package jq pour le parsing du JSON
# En cas d'ajout d'un type de capteur il faut modifier le script
# Prend en parametre l'archive a traiter

HOST=$(~/Script/GetInfo.sh HOST)
DB=$(~/Script/GetInfo.sh DB)
USER=$(~/Script/GetInfo.sh USER)
PASS=$(~/Script/GetInfo.sh PASS)
PATH_DATA=~/data

# Fonction d'insertion dans la base de donnees
function queryDB {
	QUERY="$1"
	result=$(mysql -h $HOST -D $DB -u $USER -p$PASS -e "$QUERY")
	
	result=$(echo $result | sed -e s'/s_id //'g)
	echo $result
}


echo "up To DB"
mkdir tmp 
cd tmp

# Ancien fonction pour traiter plusieurs achives
#i=0
#for arch in $(find ~/data -name *.tar.xz) ; do
#	filename=tot$i
#	mkdir $filename
#	cd $filename
#	tar xvfJ $arch
#	cd ..
#	i=$((i+1))
#done

arch=$1
tar xvfJ $PATH_DATA/$arch
JSONFILE=$(cat test.json)
ELEM_NB=$(echo $JSONFILE | jq length)
ELEM_NB=$((ELEM_NB-1))

# Parcours du fichier
for i in `seq 1 $ELEM_NB` ; do
	ELEM_ID=$(echo "$JSONFILE" | jq .[$i].probeID )
	ELEM_DATE=$(echo "$JSONFILE" | jq .[$i].date )
	#echo " $ELEM_ID $ELEM_DATE"
	JQ_PARAM=".[$i]|keys "
	JQ_RESULT=$(echo "$JSONFILE" | jq $JQ_PARAM | sed -e s'/,//'g -e s'/\"//'g )
	for key in $JQ_RESULT ; do
		ST_ID=0
		case "$key" in
			("ozone")
				ST_ID=1
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].ozone )
			;;
			("temperature")
				ST_ID=2
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].temperature )
			;;
			("airHumidity")
				ST_ID=3
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].airHumidity )
			;;
			("groundHumidity")
				ST_ID=4
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].groundHumidity )
			;;
			("waterLevel")
				ST_ID=5
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].waterLevel )
			;;
			("waterTemperature")
				ST_ID=6
				ELEM_VALUE=$(echo "$JSONFILE" | jq .[$i].waterTemperature )
			;;
		esac
		if [[ $ST_ID -gt 0 ]] ; then
			if [[ $i -lt 4 ]] ; then
				RQ="SELECT s_id from sensor where sta_id='$ELEM_ID' AND st_id='$ST_ID'"
				S_ID=$(queryDB "$RQ")
				RQ="INSERT INTO measure values (NULL,'$ELEM_DATE','$ELEM_VALUE','$S_ID')"
				queryDB "$RQ"
			fi
		fi
	done
done
rm -fr ~/tmp
