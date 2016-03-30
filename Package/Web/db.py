#!/usr/bin/python
print "Content-type: text/html"
print ""

import MySQLdb

db = MySQLdb.connect(host="srvmysql.imerir.com", user="SmartForest", passwd="LjcX7vWRMs84jJ3h", db="SmartForest")

cur = db.cursor()
cur.execute("SHOW TABLES")
for row in cur.fetchall():
	print row[0]
	print "<br>"

db.close()
