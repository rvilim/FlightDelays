import pandas as pd
import numpy as np
import sys
from datetime import datetime
from pandas.tseries.offsets import *

pd.set_option('display.max_columns', None)

years=sys.argv[1:]

# print years
weather=pd.DataFrame()
delays=pd.DataFrame()

weather=pd.read_pickle('../Weather/Data/weather_'+str(min(map(int, years))-1))

for year in years:
    weather=weather.append(pd.read_pickle('../Weather/Data/weather_'+str(year)), ignore_index=True)
    delays=delays.append(pd.read_pickle('../Data/delays_'+str(year)), ignore_index=True)

# print delays.dtypes
# delays.sort(columns=['CRSDep','OriginAirportID','AirlineID'])
# delays.to_csv('A.csv')
# delays.iloc[:10000].to_csv('B.csv')

originweather=weather
destweather=weather
prevoriginweather=weather
prevdestweather=weather

destweather=destweather.rename(columns={'TMAX': 'TMax_Dest'})
destweather=destweather.rename(columns={'TMIN': 'TMin_Dest'})
destweather=destweather.rename(columns={'PRCP': 'Prcp_Dest'})
destweather=destweather.rename(columns={'SNOW': 'Snow_Dest'})
destweather=destweather.rename(columns={'AWND': 'AWnd_Dest'})
destweather=destweather.rename(columns={'WSF2': 'WSf2_Dest'})
destweather=destweather.rename(columns={'WDF2': 'WDf2_Dest'})

prevdestweather['NEXTDAY']=prevdestweather['DATE'].apply(lambda x: x+Day())
prevdestweather=prevdestweather.rename(columns={'TMAX': 'TMax_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'TMIN': 'TMin_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'PRCP': 'Prcp_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'SNOW': 'Snow_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'AWND': 'AWnd_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'WSF2': 'WSf2_Dest_prev'})
prevdestweather=prevdestweather.rename(columns={'WDF2': 'WDf2_Dest_prev'})

originweather=originweather.rename(columns={'TMAX': 'TMax_Origin'})
originweather=originweather.rename(columns={'TMIN': 'TMin_Origin'})
originweather=originweather.rename(columns={'PRCP': 'Prcp_Origin'})
originweather=originweather.rename(columns={'SNOW': 'Snow_Origin'})
originweather=originweather.rename(columns={'AWND': 'AWnd_Origin'})
originweather=originweather.rename(columns={'WSF2': 'WSf2_Origin'})
originweather=originweather.rename(columns={'WDF2': 'WDf2_Origin'})

prevoriginweather['NEXTDAY']=prevoriginweather['DATE'].apply(lambda x: x+Day())
prevoriginweather=prevoriginweather.rename(columns={'TMAX': 'TMax_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'TMIN': 'TMin_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'PRCP': 'Prcp_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'SNOW': 'Snow_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'AWND': 'AWnd_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'WSF2': 'WSf2_Origin_prev'})
prevoriginweather=prevoriginweather.rename(columns={'WDF2': 'WDf2_Origin_prev'})

prevdestweather['DATE']=prevdestweather['DATE'].apply(lambda x: x.date())
prevdestweather['NEXTDAY']=prevdestweather['NEXTDAY'].apply(lambda x: x.date())

prevoriginweather['DATE']=prevoriginweather['DATE'].apply(lambda x: x.date())
prevoriginweather['NEXTDAY']=prevoriginweather['NEXTDAY'].apply(lambda x: x.date())

originweather['DATE']=originweather['DATE'].apply(lambda x: x.date())
destweather['DATE']=destweather['DATE'].apply(lambda x: x.date())
delays['date']=delays['CRSDep'].apply(lambda x: x.date())

# print depweather['AIRPORT_ID']
# print delays['OriginAirportID']
# print depweather.dtypes
# print delays.dtypes

# print originweather
# A=originweather[originweather.AIRPORT_ID==14771]
# A=A[A.DATE=='2010-01-01']
# A.to_csv('B.csv')

delays=pd.merge(delays, originweather, left_on=['date', 'OriginAirportID' ], right_on=['DATE', 'AIRPORT_ID'])
delays=pd.merge(delays, prevoriginweather, left_on=['date', 'OriginAirportID'], right_on=['NEXTDAY', 'AIRPORT_ID'])

delays=pd.merge(delays, destweather, left_on=['date', 'DestAirportID' ], right_on=['DATE', 'AIRPORT_ID'])
delays=pd.merge(delays, prevdestweather, left_on=['date', 'DestAirportID'], right_on=['NEXTDAY', 'AIRPORT_ID'])

# jfk_airport_id=12478
# sfo_airport_id=14771
#
# delays=delays[delays.DestAirportID == sfo_airport_id]
# delays=delays[delays.OriginAirportID == jfk_airport_id]
# delays.sort(columns=['DayNum'], inplace=True)


to_drop = [x for x in delays if x.endswith('_y')]
delays.drop(to_drop, axis=1, inplace=True)

to_drop = [x for x in delays if x.endswith('_x')]
delays.drop(to_drop, axis=1, inplace=True)

delays.drop('NEXTDAY', axis=1, inplace=True)
delays.drop('date', axis=1, inplace=True)

delays.to_pickle('../Data/delays_weather_'+str(year))

# delays.iloc[:10000].to_csv('A.csv')
# delays.drop('DATE', axis=1, inplace=True)
# delays.drop('date', axis=1, inplace=True)
# delays.drop('AIRPORT_ID', axis=1, inplace=True)

