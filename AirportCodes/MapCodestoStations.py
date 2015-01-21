import pandas as pd
import numpy as np
import csv as csv
from math import radians, cos, sin, asin, sqrt
import sys

def haversine(lon1, lat1, lon2, lat2):
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6367 * c
    return km

def getnearest(WeatherStations, row):
    airport_id=row[0]
    airportname=row[1]
    airportlat=row[2]
    airportlon=row[3]

    mindist=1000000
    for stationid, stationlat, stationlon, stationname in zip(WeatherStations.values[:,0], WeatherStations.values[:,1],WeatherStations.values[:,2],WeatherStations.values[:,3]):
        distance=haversine(airportlon, airportlat, stationlon, stationlat)
        if(distance<mindist):
            mindist=distance
            closeststationname=stationname
            closeststationid=stationid
            # print airportlon, airportlat, stationlon, stationlat
            
    print mindist, airport_id, closeststationid
        
    return 1
UsedAirportCodes=pd.read_csv('airports')
    
AirportCodes=pd.read_csv('AirportCodes.csv', usecols=['AIRPORT_ID', 'DISPLAY_AIRPORT_NAME', 'LATITUDE', 'LONGITUDE'])
WeatherStations=pd.read_fwf('WeatherStations.txt', colspecs=[(0,11), (12,20), (21,30), (31,37), (38,40), (41,71), (72,75), (76,79), (80,85)],
                                                   names=["Station_ID","Latitude", "Longitude", "Elevation", "State", "Name", 
                                                          "GSN Flag","HCN/CRN Flag", "WMO ID"])
AirportCodes=AirportCodes.merge(UsedAirportCodes, on='AIRPORT_ID').drop_duplicates(subset='AIRPORT_ID')
        
WeatherStations=WeatherStations.loc[:,['Station_ID', 'Latitude', 'Longitude','Name']]

A=AirportCodes.apply(lambda x: getnearest(WeatherStations,x),axis=1)