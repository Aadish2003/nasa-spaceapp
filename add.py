import mysql.connector

dbr = mysql.connector.connect(host='localhost',
                              user='root',
                              database='nasa',
                              password=''
                              )
cr = dbr.cursor()

f='nasa.sql'
with open(f,'r') as file:
    s=file.read()

cr.execute(s)

print('done')