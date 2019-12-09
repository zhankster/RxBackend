import pyodbc

print "Database Connectivity Test\n"

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=IHSSQL1;DATABASE=RXBackend;Trusted_Connection=yes')

cur = conn.cursor()

cur.execute("SELECT count(*) as cnt from role")
data = cur.fetchone()

print "Row Count %s" % data