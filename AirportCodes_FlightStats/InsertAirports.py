import json
import pymysql as mdb

# query="INSERT INTO Airports (Airport_ID, Position) VALUES ("+str(int(row['AIRPORT_ID']))+", PointFromText(CONCAT('POINT(','"+str(row['LATITUDE'])+"',' ','"+str(row['LONGITUDE'])+"',')')));"
# cur.execute(query)
    
# conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
# cur = conn.cursor()

jsondata=open('AirlinesJson.json','r')

myjson=""

for line in jsondata:
    myjson=myjson+line

data = json.loads(myjson)


for airline in data["airlines"]:
    if(airline["active"]==True):
        print airline
    