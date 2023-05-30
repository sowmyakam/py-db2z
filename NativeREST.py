import requests
import sys
import xlsxwriter

if len(sys.argv) < 3:
   print("Usage: %s <userid> <password> " % (sys.argv[0]))
   exit(-1)

workbook = xlsxwriter.Workbook('simple-excel.xlsx')
worksheet = workbook.add_worksheet()

cell_format0 = workbook.add_format({'bold': True, 'font_color': 'red'})

row = 0
worksheet.write(row,0,"CREATOR",cell_format0)
worksheet.write(row,1,"NAME",cell_format0)

row = row + 1

userid=sys.argv[1]
password=sys.argv[2]

collection='SYSIBMSERVICE'
service='selectAllTables'

#Native REST port for Db2 is the same as the DDF Port. 
#if using https use SECPORT. For http use TCPPORT
url = 'https://<hostname>:<secport>/services/'+collection+'/'+service
auth = requests.auth.HTTPBasicAuth(userid,password)

#If unsure of how the secure port auth works, use verify=False in the request header below. 
#If you have the cert available for auth, then dont specify the verify header. Default for verify is true.
resp = requests.post(url,auth=auth,verify=False, headers = {"Content-Type": "application/json", "Accepts":"application/json"})

data = resp.json()

for table in data['ResultSet Output']:
   worksheet.write(row,0,table['CREATOR'].strip())
   worksheet.write(row,1,table['NAME'].strip())
   row = row + 1

workbook.close()
