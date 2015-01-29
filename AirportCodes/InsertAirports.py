import pandas as pd
import numpy as np
import csv as csv
import pymysql as mdb
import urllib2
from datetime import datetime
import time


def doquery(cur, row):

    query="INSERT INTO Airports (Airport_ID, Position) VALUES ("+str(int(row['AIRPORT_ID']))+", PointFromText(CONCAT('POINT(','"+str(row['LATITUDE'])+"',' ','"+str(row['LONGITUDE'])+"',')')));"
    cur.execute(query)
    
    

conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
cur = conn.cursor()

AirportCodes=pd.read_csv('AirportCodes.csv', usecols=['AIRPORT_ID', 'LATITUDE', 'LONGITUDE'])

UsedAirportCodes=pd.read_csv('airports')

AirportCodes.loc[:,['AIRPORT_ID']]=AirportCodes.loc[:,['AIRPORT_ID']].astype('uint32')
UsedAirportCodes.loc[:,['AIRPORT_ID']]=UsedAirportCodes.loc[:,['AIRPORT_ID']].astype('uint32')

A=AirportCodes.merge(UsedAirportCodes, on='AIRPORT_ID').drop_duplicates(subset='AIRPORT_ID')

A.apply(lambda x: doquery(cur, x),axis=1)
conn.commit()
cur.close()
conn.close()