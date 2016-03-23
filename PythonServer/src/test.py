#! /usr/bin/env python

import MySQLdb as mdb
import smtplib
import string
from random import sample, choice
from subprocess import Popen,PIPE
import md5

error=0
PATH_SCRIPT="../../Script"
#HOST=Popen("print (Hello WORl)", stdout=PIPE, shell=True).communicate()[0]
HOST=Popen(PATH_SCRIPT+"/GetInfo.sh HOST", stdout=PIPE, shell=True).stdout.read()
DB=Popen(PATH_SCRIPT+"/GetInfo.sh DB", stdout=PIPE, shell=True).stdout.read()
PASSWORD=Popen(PATH_SCRIPT+"/GetInfo.sh PASS", stdout=PIPE, shell=True).stdout.read()
USER=Popen(PATH_SCRIPT+"/GetInfo.sh USER", stdout=PIPE, shell=True).stdout.read()

# Verification du login
# Boolean
def isLogin(login):
    valid = False
    try:
        con = mdb.connect(str(HOST), USER, PASSWORD, DB)
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

toto=isLogin("abe")
print toto
