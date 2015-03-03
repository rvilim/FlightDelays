import pandas as pd
import numpy as np    

years=[2010, 2011, 2012, 2013, 2014]
fulldelays=pd.DataFrame()

for year in years:
  fulldelays=fulldelays.append(pd.read_pickle('../Data/delays_weather_'+str(year)))

# fulldelays.loc[:,["OriginAirportID","DestAirportID"]].drop_duplicates().apply(lambda x: getnumflights(x, fulldelays), axis=1)
numflights=fulldelays.groupby(["OriginAirportID","DestAirportID"]).size()
numflights[numflights>1000].to_csv('flights.csv')
