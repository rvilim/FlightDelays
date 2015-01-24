import pandas as pd
import numpy as np
import csv as csv
import sys
from datetime import datetime

year=sys.argv[1]

observations=pd.DataFrame()
weather=pd.DataFrame()

parse = lambda x: datetime.strptime(x, '%Y%m%d')

stations=pd.read_csv('Data/CSVs/airportsstations.csv', usecols=['AIRPORT_ID','STATION'])

observations=pd.read_csv('Data/CSVs/'+str(year)+'.csv',header=None,names=['STATION', 'DATE', 'ELEMENT', 'DATA', 'M', 'Q', 'S', 'OBS'],
parse_dates = ['DATE'], date_parser=parse)

observations['STATION'] = observations['STATION'].map(lambda x: x.upper())

observations=pd.merge(observations, stations, on='STATION')

TMAX=observations[observations['ELEMENT']=='TMAX'].loc[:,['STATION','DATE','DATA']]
TMAX.rename(columns={'DATA': 'TMAX'}, inplace=True)

TMIN=observations[observations['ELEMENT']=='TMIN'].loc[:,['STATION','DATE','DATA']]
TMIN.rename(columns={'DATA': 'TMIN'}, inplace=True)

PRCP=observations[observations['ELEMENT']=='PRCP'].loc[:,['STATION','DATE','DATA']]
PRCP.rename(columns={'DATA': 'PRCP'}, inplace=True)

SNOW=observations[observations['ELEMENT']=='SNOW'].loc[:,['STATION','DATE','DATA']]
SNOW.rename(columns={'DATA': 'SNOW'}, inplace=True)

AWND=observations[observations['ELEMENT']=='AWND'].loc[:,['STATION','DATE','DATA']]
AWND.rename(columns={'DATA': 'AWND'}, inplace=True)

WSF2=observations[observations['ELEMENT']=='WSF2'].loc[:,['STATION','DATE','DATA']]
WSF2.rename(columns={'DATA': 'WSF2'}, inplace=True)

WDF2=observations[observations['ELEMENT']=='WDF2'].loc[:,['STATION','DATE','DATA']]
WDF2.rename(columns={'DATA': 'WDF2'}, inplace=True)


# WDFS=observations[observations['ELEMENT']=='WDF5'].loc[:,['STATION','DATE','DATA']]
# WDFS.rename(columns={'DATA': 'WDF5'}, inplace=True)

# This looks incredibly dumb, but what I am doing is multiplying the NOAA observations
# by various scales to ge them into celcius and km/h

TMAX.TMAX=TMAX.TMAX/10.0
TMIN.TMIN=TMIN.TMIN/10.0
PRCP.PRCP=PRCP.PRCP/10.0
SNOW.SNOW=SNOW.SNOW/10.0
# SNWD.SNWD=SNWD.SNWD/10.0
AWND.AWND=AWND.AWND*3.6/10.0
WSF2.WSF2=WSF2.WSF2*3.6/10.0
# WSF5.WSF5=WSF5.WSF5*3.6/10.0

# Now that we have each column, we merge them into the weather data frame with outer joins
weather=TMAX
weather=pd.merge(weather, TMIN, on=['STATION','DATE'], how='outer')
weather=pd.merge(weather, PRCP, on=['STATION','DATE'], how='outer')
weather=pd.merge(weather, SNOW, on=['STATION','DATE'], how='outer')
weather=pd.merge(weather, AWND, on=['STATION','DATE'], how='outer')
weather=pd.merge(weather, WSF2, on=['STATION','DATE'], how='outer')
weather=pd.merge(weather, WDF2, on=['STATION','DATE'], how='outer')

weather = weather[np.isfinite(weather['TMAX'])&np.isfinite(weather['TMIN'])&np.isfinite(weather['PRCP'])&np.isfinite(weather['SNOW'])&
                  np.isfinite(weather['AWND'])&np.isfinite(weather['WSF2'])&np.isfinite(weather['WDF2'])]
            

weather=pd.merge(weather, stations, on='STATION')
# weather.to_pickle('Data/weather_'+str(year))
weather.to_csv('A.csv')