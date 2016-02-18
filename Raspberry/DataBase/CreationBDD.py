import sqlite3

#creation d'une connexion a la base de donnée des balise
connection = sqlite3.connect("./Database/Balise.db")

#creation d'un curseur pour interagir avec la basse de donnée
cursor = connection.cursor()

#création de la table balise dans la basse de donnee
cursor.execute('''CREATE TABLE `balise` (
                  `b_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  `b_nom`	INTEGER NOT NULL UNIQUE
                  )''')

#creation de la table releve dans la base de donnee et liaison entre balise et relevee
cursor.execute(''' CREATE TABLE `releve` (
                  `r_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                  `r_date`	NUMERIC NOT NULL,
                  `r_ozone`	INTEGER NOT NULL,
                  `r_temperature`	REAL NOT NULL,
                  `r_humidite`	REAL NOT NULL,
                  `r_hygrometrie`	REAL NOT NULL,
                  `r_balise`	INTEGER NOT NULL,
                  FOREIGN KEY(`r_balise`) REFERENCES balise(`b_id`)
                  )''')
