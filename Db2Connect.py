import ibm_db
import configparser

config = configparser.ConfigParser()
config.readfp(open('<Pathto>/SystemInfo.config'))
location = config.get('Db2EC', 'location')
host = config.get('Db2EC', 'host')
port = config.get('Db2EC', 'port')
user = config.get('Db2EC', 'user')
passwd = config.get('Db2EC', 'password')

conn_str='database='+location+';hostname='+host+';port='+port+';uid='+user+';pwd='+passwd+';OnlyUseBigPackages=1;AUTHENTICATION=SERVER;<addl. JDBC properties as needed>'

#From distributed
conn = ibm_db.connect(conn_str,'','')

#From USS on Z
#conn = ibm_db.connect('','','')

if conn:
    sql = "SELECT * FROM SYSIBM.SYSTABLES FETCH FIRST 10 ROWS ONLY"
    stmt = ibm_db.exec_immediate(conn,sql)
    result = ibm_db.fetch_both(stmt)
    while(result):
        print(result[1].strip()+"."+result[0].strip())
        result = ibm_db.fetch_both(stmt)

    ibm_db.close(conn)