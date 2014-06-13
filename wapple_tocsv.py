import sqlite3 as lite
import sys
con = None

try:
	con = lite.connect('wapple.db')
	cur = con.cursor()

	cur.execute("select Name, url, application, category from features inner join Sites on sites.id = features.siteid;")
	
	rows = cur.fetchall()
		
	for row in rows:
		print "{0},{1},{2},{3}".format(row[0],row[1],row[2],row[3])  
		
except lite.Error, e:

	print "Error %s:" % e.args[0]
	sys.exit(1)
	
finally:

	if con:
		con.close()		
