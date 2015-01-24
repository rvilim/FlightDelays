import pandas as pd
import numpy as np
import csv as csv
from pandas.io import sql
import pymysql as mdb
import urllib2
from datetime import datetime
import time
def getforecast(station):
    lat=station['LATITUDE']
    lon=station['LONGITUDE']
    airport_id=station['AIRPORT_ID']
    
    url='http://api.wunderground.com/api/1e514cfbdae56795/forecast10day/q/'+str(lat)+','+str(lon)+'.json'
    
    print url
    
    f = urllib2.urlopen(url)
    json_forecast = f.read()
    print airport_id
    time.sleep(61/100)
    return json_forecast
con = mdb.connect('localhost', 'root', '', 'weather') #host, user, password, #database

AirportCodes=pd.read_csv('AirportCodes.csv', usecols=['AIRPORT_ID', 'LATITUDE', 'LONGITUDE'])

UsedAirportCodes=pd.read_csv('airports')

AirportCodes.loc[:,['AIRPORT_ID']]=AirportCodes.loc[:,['AIRPORT_ID']].astype('uint32')
UsedAirportCodes.loc[:,['AIRPORT_ID']]=UsedAirportCodes.loc[:,['AIRPORT_ID']].astype('uint32')

A=AirportCodes.merge(UsedAirportCodes, on='AIRPORT_ID').drop_duplicates(subset='AIRPORT_ID')

A['json_forecast']=A.apply(lambda x: getforecast(x),axis=1)
A['forecast_date']=A.apply(lambda x: np.datetime64(datetime.now()), axis=1)

A.to_sql('forecasts', con, 'mysql', index=False,if_exists='append')
