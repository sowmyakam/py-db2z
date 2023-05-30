import ibm_db
import configparser


config = configparser.ConfigParser()
config.readfp(open('<PATHTO>/SystemInfo.config'))
location = config.get('Db2EC', 'location')
host = config.get('Db2EC', 'host')
port = config.get('Db2EC', 'port')
user = config.get('Db2EC', 'user')
passwd = config.get('Db2EC', 'password')

conn_str='database='+location+';hostname='+host+';port='+port+';uid='+user+';pwd='+passwd+';OnlyUseBigPackages=1;AUTHENTICATION=SERVER;<addl. JDBC props>'

try:
   conn=ibm_db.connect(conn_str,'','')
except:
   print("Connect to %s failed: %s" % ("Db2 for zOS",ibm_db.conn_errormsg()))
   exit
else:
   print("Succesfully connected to Db2 for zOS" )

db2_util = '<UNIQUE ID FOR UTIL>'
restartUtil = 'NO'
runstats_cmd = '<RUNSTATS COMMAND>'
msg = 0

stmt, db2_util, restartUtil, runstats_cmd, msg = \
ibm_db.callproc(conn, 'SYSPROC.DSNUTILU',( db2_util, restartUtil, runstats_cmd, msg ) )

stmt1 = stmt

while stmt1:
   # result set available
   print("Result set")

   row = ibm_db.fetch_assoc(stmt1)
   while row:
      print(row)
      row = ibm_db.fetch_assoc(stmt1)

   stmt1 = ibm_db.next_result(stmt)

try:
   ibm_db.commit(conn)
except:
   print("COMMIT failed: ",ibm_db.stmt_errormsg())

try:
   ibm_db.close(conn)
except:
   print("close connection failed: ",ibm_db.stmt_errormsg())