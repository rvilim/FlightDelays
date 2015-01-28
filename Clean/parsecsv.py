import pandas as pd
import numpy as np
import csv as csv
import sys

import matplotlib.pyplot as plt
from datetime import datetime
from random import sample

from sklearn.ensemble import RandomForestClassifier

import holidays

def distancetoholiday(flight):

    
    daysoff=holidays.getholidays(flight['CRSDep'].year,flight['OriginState'])
    # This does a list comprehension to get the distance from each holiday
    holidaydeltas=[(flight['CRSDep'].date()-holiday).days for holiday in daysoff]

    # This then converts that to a numpy array
    # then takes the absolute value of all the variables in that numpy array, then gets the location of the closest
    # and finally returns the number of days to the closest holiday. Whew!

    
    return holidaydeltas[np.argmin(np.absolute(np.asarray(holidaydeltas)))]
    # return 1
    
def readdelays(month, year):
    delays=pd.read_csv('../Data/CSVs/On_Time_On_Time_Performance_'+str(year)+'_'+str(month)+'.csv',
                        usecols=['FlightDate','AirlineID','FlightNum','OriginAirportID','OriginState', 'DestAirportID', 'DestState', 'CRSDepTime','DepTime','DepDelay', 
                                 'CRSArrTime', 'ArrTime','ArrDelay','CarrierDelay','WeatherDelay','NASDelay','SecurityDelay','LateAircraftDelay',
                                 'Cancelled','Diverted','CRSElapsedTime','ActualElapsedTime','Distance','Month', 'DayofMonth', 'DayOfWeek'])    

    return delays

def fillcancelled(row):
    if(row['Cancelled']=='1'):
        row['ArrTime']='-9999'
        row['ArrDelay']='-9999'
        row['ActualElapsedTime']='-9999'
    
    return row
    
def cleandelays(delays,year):
        
    delays=delays[delays['DepTime']!=2400]
    delays=delays[delays['ArrTime']!=2400]
    
    delays=delays[delays['CRSDepTime']!=2400]
    delays=delays[delays['CRSArrTime']!=2400]
    
    delays['CarrierDelay']=delays['CarrierDelay'].fillna(0)
    delays['WeatherDelay']=delays['WeatherDelay'].fillna(0)
    delays['NASDelay']=delays['NASDelay'].fillna(0)
    delays['SecurityDelay']=delays['SecurityDelay'].fillna(0)
    delays['LateAircraftDelay']=delays['LateAircraftDelay'].fillna(0)    
    delays['Cancelled']=delays['Cancelled'].fillna(0)
        
    delays=delays.apply(fillcancelled,axis=1)
    
    delays=delays.dropna()
    
    delays.loc[:,['AirlineID']]=delays.loc[:,['AirlineID']].astype('uint32')
    delays.loc[:,['FlightNum']]=delays.loc[:,['FlightNum']].astype('uint16')
    delays.loc[:,['OriginAirportID']]=delays.loc[:,['OriginAirportID']].astype('uint32')
    delays.loc[:,['DestAirportID']]=delays.loc[:,['DestAirportID']].astype('uint32')
    delays.loc[:,['CRSDepTime']]=delays.loc[:,['CRSDepTime']].astype('uint16')
    delays.loc[:,['DepDelay']]=delays.loc[:,['DepDelay']].astype('int16')
    delays.loc[:,['CRSArrTime']]=delays.loc[:,['CRSArrTime']].astype('uint16')
    delays.loc[:,['ArrDelay']]=delays.loc[:,['ArrDelay']].astype('int16')
    delays.loc[:,['CarrierDelay']]=delays.loc[:,['CarrierDelay']].astype('int16')
    delays.loc[:,['WeatherDelay']]=delays.loc[:,['WeatherDelay']].astype('int16')
    delays.loc[:,['NASDelay']]=delays.loc[:,['NASDelay']].astype('int16')
    delays.loc[:,['SecurityDelay']]=delays.loc[:,['SecurityDelay']].astype('int16')
    delays.loc[:,['LateAircraftDelay']]=delays.loc[:,['LateAircraftDelay']].astype('int16')
    delays.loc[:,['Cancelled']]=delays.loc[:,['Cancelled']].astype('uint8')
    delays.loc[:,['CRSElapsedTime']]=delays.loc[:,['CRSElapsedTime']].astype('uint32')
    delays.loc[:,['ActualElapsedTime']]=delays.loc[:,['ActualElapsedTime']].astype('uint32')
    delays.loc[:,['Distance']]=delays.loc[:,['Distance']].astype('uint32')
    delays['DayOfMonth']=delays.loc[:,['DayofMonth']].astype('uint8')
    delays=delays.drop('DayofMonth', axis=1) # Note the change in Capitalization, I basically just renamed the column here
    delays.loc[:,['Month']]=delays.loc[:,['Month']].astype('uint8')
    delays.loc[:,['DayOfWeek']]=delays.loc[:,['DayOfWeek']].astype('uint8')-1
        
    # Turn the CRS Departure time into a Datetime
    delays['CRSDepTime']=delays['CRSDepTime'].astype('int').astype('str').str.pad(4,'left').str.replace(' ','0')
    delays['CRSDepTime']=delays['CRSDepTime'].str[0:2]+':'+delays['CRSDepTime'].str[2:4]
    delays['CRSArrTime']=delays['CRSArrTime'].astype('int').astype('str').str.pad(4,'left').str.replace(' ','0')
    delays['CRSArrTime']=delays['CRSArrTime'].str[0:2]+':'+delays['CRSArrTime'].str[2:4]


    delays['CRSDep']=pd.to_datetime(delays.FlightDate+' '+delays.CRSDepTime ,'%Y-%m-%d %H:%M')
    delays['CRSArr']=pd.to_datetime(delays.FlightDate+' '+delays.CRSArrTime ,'%Y-%m-%d %H:%M')

    delays['DayNum']=delays['CRSDep'].apply(lambda d: datetime.strftime(d, '%j')).astype('uint16')
    delays['DepMidnightHours']=delays['CRSDep'].apply(lambda d: int(datetime.strftime(d, '%H'))).astype('uint16')
    delays['ArrMidnightHours']=delays['CRSArr'].apply(lambda d: int(datetime.strftime(d, '%H'))).astype('uint16')

    delays['DaysToHoliday']=delays.apply(lambda x: distancetoholiday(x),axis=1)

    delays=delays.drop('OriginState', axis=1)
    delays=delays.drop('DestState', axis=1)
    delays=delays.drop('FlightDate', axis=1)    
    delays=delays.drop('CRSDepTime', axis=1)
    delays=delays.drop('CRSArrTime', axis=1)

    
    return delays

years=sys.argv[1:]

delays=pd.DataFrame()

for year in years:
    maxmonth=12
    
    if(year=='2014'):
        maxmonth=11
        
    for month in xrange(1,maxmonth+1):
        print year, month
        delaymonth=readdelays(month,year)
        delaymonth=cleandelays(delaymonth,year)
        delays=delays.append(delaymonth, ignore_index=True)


    # delays.to_csv('A.csv')
    delays.to_pickle('../Data/delays_'+str(year))
