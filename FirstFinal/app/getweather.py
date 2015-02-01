import pandas as pd
import numpy as np
import csv as csv
from pandas.io import sql
import pymysql as mdb
import urllib2
import datetime
import time
import json

def getjson(lat, lon):

    url='http://api.wunderground.com/api/1e514cfbdae56795/forecast10day/q/'+str(lat)+','+str(lon)+'.json'

    print url

    f = urllib2.urlopen(url)
    json_forecast = f.read()
    return json_forecast


def parsejson(flightdate,jsondata):
    daysinfuture=(flightdate.date()-datetime.date.today()).days
    # print daysinfuture
    
    data = json.loads(jsondata)
        
    weather={}

    weather["POP"] = int(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['pop'])
    weather["TMAX"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['high']['celsius'])
    weather["TMIN"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['low']['celsius'])
    weather["SNOW"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['snow_allday']['cm'])
    weather["PRCP"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['qpf_allday']['mm'])
    weather["AWND"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['avewind']['kph'])
    weather["WSF2"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['maxwind']['kph'])
    weather["WDF2"] = float(data['forecast']['simpleforecast']['forecastday'][daysinfuture]['maxwind']['degrees'])
    
    return weather
    
def getforecast(flightdate, Airport_ID):
    conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
    cur = conn.cursor()

    query="SELECT X(Position),Y(Position) FROM AIRPORTS WHERE Airport_ID="+str(Airport_ID)+";"
    cur.execute(query)
    location=cur.fetchone()
    lat=location[0]
    lon=location[1]
    
    weatherprediction=getjson(lat,lon)
    flightdayweather=parsejson(flightdate,weatherprediction)
    prevdayweather=parsejson(flightdate-datetime.timedelta(days=1),weatherprediction)
    
    return [prevdayweather, flightdayweather]
    
    
