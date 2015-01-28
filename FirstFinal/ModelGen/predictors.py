import matplotlib

matplotlib.use('Agg')


import pandas as pd
import numpy as np
import csv as csv
import sys

import matplotlib.pyplot as plt
from datetime import datetime
from random import sample

from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import OneHotEncoder

from sklearn import svm
from sklearn import cross_validation

from sklearn.metrics import roc_curve, auc, f1_score

from sklearn import tree

from scipy import interp

from sklearn.externals import joblib

def chunk_arrivals(row):
    if(row['Cancelled']==1):
        return -1
        
    if(row['ArrDelay']<=15):
        return 0
        
    return int(np.ceil(row['ArrDelay']/15.0))-1

def get_vectorized(catarray, enc):
    catarray=[[i] for i in catarray]
    return enc.transform(catarray).toarray()

def balance_weights(y):
    """Compute sample weights such that the class distribution of y becomes
       balanced.
    Parameters
    ----------
    y : array-like
        Labels for the samples.
    Returns
    -------
    weights : array-like
        The sample weights.
    """
    y = np.asarray(y)
    y = np.searchsorted(np.unique(y), y)
    bins = np.bincount(y)
    weights = 1. / bins.take(y)
    weights *= bins.min()
    return weights

def genmodel(delays, origin_airport_id, dest_airport_id):
    delays=fulldelays[delays.OriginAirportID == origin_airport_id]
    delays=delays[delays.DestAirportID == dest_airport_id]
    
    delays=delays[(delays['Diverted']==0)]

    delays['ArrDelayGroup']=delays.apply(chunk_arrivals, axis=1)

    # Get the encoder for the airline
    airlines=list(np.unique(delays['AirlineID'].apply(lambda x: [int(x)])))
    # dephours=list(np.unique(delays['DepMidnightHours'].apply(lambda x: [int(x)])))
    # arrhours=list(np.unique(delays['ArrMidnightHours'].apply(lambda x: [int(x)])))
    dayofweek=list(np.unique(delays['DayOfWeek'].apply(lambda x: [int(x)])))
    dayofmonth=list(np.unique(delays['DayOfMonth'].apply(lambda x: [int(x)])))
    month=list(np.unique(delays['Month'].apply(lambda x: [int(x)])))

    Airlinesenc = OneHotEncoder()
    DayOfWeekenc = OneHotEncoder()
    MonthEnc = OneHotEncoder()
    DayOfMonthEnc = OneHotEncoder()

    # dephoursenc = OneHotEncoder()
    # arrhoursenc = OneHotEncoder()

    Airlinesenc.fit(airlines)
    DayOfWeekenc.fit(dayofweek)
    MonthEnc.fit(month)
    DayOfMonthEnc.fit(dayofmonth)

    # dephoursenc.fit(dephours)
    # arrhoursenc.fit(arrhours)

    vec_Airlines=get_vectorized(delays['AirlineID'].values,Airlinesenc)
    vec_DayOfWeek=get_vectorized(delays['DayOfWeek'].values,DayOfWeekenc)
    vec_Month=get_vectorized(delays['Month'].values,MonthEnc)
    vec_DayOfMonth=get_vectorized(delays['DayOfMonth'].values,DayOfMonthEnc)

    # vec_dephours=get_vectorized(delays['DepMidnightHours'].values,dephoursenc)
    # vec_arrhours=get_vectorized(delays['ArrMidnightHours'].values,arrhoursenc)
    # 'Month', 'DayOfWeek', 'DayOfMonth', 'DayNum', 

    featurelabels=['DepMidnightHours', 'ArrMidnightHours', 'DaysToHoliday',
                   'Prcp_Dest','Snow_Dest','AWnd_Dest','WSf2_Dest','WDf2_Dest',
                   'Prcp_Dest_prev','Snow_Dest_prev','AWnd_Dest_prev','WSf2_Dest_prev','WDf2_Dest_prev',
                   'Prcp_Origin','Snow_Origin','AWnd_Origin','WSf2_Origin','WDf2_Origin',
                   'Prcp_Origin_prev','Snow_Origin_prev','AWnd_Origin_prev','WSf2_Origin_prev','WDf2_Origin_prev'
                  ]

    X=delays.loc[:,featurelabels].values
    X=np.hstack((X,vec_Airlines))
    X=np.hstack((X,vec_DayOfWeek))
    X=np.hstack((X,vec_Month))
    X=np.hstack((X,vec_DayOfMonth))

    for i in range(0,len(vec_Airlines[0])):
        featurelabels.append('Airlineid'+str(i))

    for i in range(0,len(vec_DayOfWeek[0])):
        featurelabels.append('DayOfWeek'+str(i))
    
    for i in range(0,len(vec_Month[0])):
        featurelabels.append('Month'+str(i))
    
    for i in range(0,len(vec_DayOfMonth[0])):
        featurelabels.append('DayOfMonth'+str(i))

    print featurelabels

    y=delays['ArrDelayGroup'].values

    classifier = GradientBoostingClassifier(n_estimators=100, max_features=63, min_samples_split=57, max_depth=4, min_samples_leaf=14)
    classifier = classifier.fit( X, y)

    joblib.dump(classifier, "classifiers/"+str(origin_airport_id)+'->'+str(dest_airport_id), comrpess=3)

# Infile is of the format
# year1 year2 year3 year4
# originairportd1 destairportid1
# originairportd2 destairportid2
# originairportd3 destairportid3
# originairportd4 destairportid4    

infile=sys.argv[1]

with open(infile, 'rb') as csvfile:
    routereader = csv.reader(csvfile, delimiter=',', quotechar='|')
    years = next(routereader)
    
    fulldelays=pd.DataFrame()

    print 'Reading ...'
    for year in years:
        fulldelays=fulldelays.append(pd.read_pickle('../../Data/delays_weather_'+str(year)))
        
    for row in routereader:
        origin_airport_id=int(row[0])
        dest_airport_id=int(row[1])
        print 'Predicting '+row[0]+ ' ---> '+ row[1]+ ' ...'
        genmodel(fulldelays, origin_airport_id, dest_airport_id)


