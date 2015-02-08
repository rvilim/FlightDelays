import json
import pymysql as mdb
import os
import urllib, json
import time

conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database

query="select Airport_ID, X(Position), Y(Position), Airport_Cityname from Airports;"
cur = conn.cursor()
cur.execute(query)

rows=cur.fetchall()

for row in rows:
    print str(row[2])+"/"+str(row[1])+"/"+str(row[3])
    
    url="https://api.flightstats.com/flex/airports/rest/v1/json/withinRadius/"+str(row[2])+"/"+str(row[1])+"/2?appId=bd500382&appKey=a43d87e86904446f95123cdac297e934"
    jsonurl = urllib.urlopen(url)
    text = json.loads(jsonurl.read())
    
    if(len(text['airports'])>1):
        print "********************************"
        print text['airports']
        print "********************************"
    
    elif(len(text['airports'])==0):
        print "No Airports"
    
    else:
        sql="UPDATE Airports SET fscode=\'"+text["airports"][0]["fs"]+"\' WHERE Airport_ID="+str(row[0])+";"
        cur.execute(sql)

    # time.sleep(5)
conn.commit()    