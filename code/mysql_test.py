# server_version.py - retrieve and display database server version

import MySQLdb

conn = MySQLdb.connect (host = "192.168.43.83",
                        user = "pratik",
                        passwd = "hello",
                        db = "parkmandu")

a = 2
with conn:
	cursor = conn.cursor ()
	cursor.execute("UPDATE park SET occupied = '"+str(a)+"' WHERE mall = 'Kathmandu Mall'")
cursor.close ()
conn.close ()
