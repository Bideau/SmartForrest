

Remplir le fichier config.ini avec :

HOST pour l'adresse du serveur mysql
DB pour le nom de la base de donnees
USER pour l'utilisateur de la base de donnees
PASSWORD pour le mot de passe de l'utilisateur
WEBPATH pour le chemin vers le serveur web de Smartforest
INTERFACE pour l'interface utiliser par le serveur

Un site Web a copier dans le repertoire necessaire pour que le serveur Web puisse le lancer.
Un serveur python lancer automatiquement par le Makefile avec la commande make.
Les fichiers Scripts qui sont deployer sur le serveur et sur le raspberry.

##################
## Installation ##
##################

1) Remplir le fichier config.ini

2) Lancer make mysql (mise en place du site web et creation complete de la base de donnees)

3) Lancer make (configuration de l'adresse ip et lancement du serveur python)
