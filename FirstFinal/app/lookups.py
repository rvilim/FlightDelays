import pymysql as mdb

def LookupAirline(AirlineFsCode):
    conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
    cur = conn.cursor()
    
    query="SELECT * FROM Airlines WHERE fscode=\'"+str(AirlineFsCode)+"\';"

    cur.execute(query)

    row=cur.fetchone()

    if(row is not None):
        return row
    else:
        print "No rows returned from LookupAirline"
        return None
        
def LookupAirport(AirportFsCode):
    conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
    cur = conn.cursor()
    
    query="SELECT Airport_ID, Airport_Code, Airport_Cityname FROM Airports WHERE fscode=\'"+str(AirportFsCode)+"\';"

    cur.execute(query)

    row=cur.fetchone()

    if(row is not None):
        return row
    else:
        print "No rows returned from LookupAirport"
        return None
        