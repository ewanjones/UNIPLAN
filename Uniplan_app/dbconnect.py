import MySQLdb

def connection():
	conn = MySQLdb.connect(host="localhost",
							user="root",
							passwd='cross1994',
							db="uniplan")
	c =  conn.cursor()
	return c, conn

