import json
from pprint import pprint
import sys
import pymysql as mdb

jsonfile=sys.argv[1]

json_data=open(jsonfile)

Airport_ID=jsonfile.split("->")[0].split("Legend_")[1]
Dest_Airport_ID=jsonfile.split("->")[1].split(".json")[0]
data = json.load(json_data)
json_data.close()



sql=""
for Airline in data["Airlines"]:
    sql=sql+"INSERT INTO Routes_Airline VALUES ("+str(Airport_ID)+", "+str(Dest_Airport_ID)+", "+str(Airline[0])+");\n"
#
# for DayOfWeek in data["DayOfWeek"]:
#     sql=sql+"INSERT INTO Routes_DayOfWeek VALUES ("+str(Airport_ID)+", "+str(Dest_Airport_ID)+", "+str(DayOfWeek[0])+");"
#
# for DayOfMonth in data["DayOfMonth"]:
#     sql=sql+"INSERT INTO Routes_DayOfMonth VALUES ("+str(Airport_ID)+", "+str(Dest_Airport_ID)+", "+str(DayOfMonth[0])+");"
#
# for Month in data["Month"]:
#     sql=sql+"INSERT INTO Routes_Month VALUES ("+str(Airport_ID)+", "+str(Dest_Airport_ID)+", "+str(Month[0])+");"

#conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
#cur = conn.cursor()
print sql
#cur.execute(sql)
#conn.commit()
#conn.close()
