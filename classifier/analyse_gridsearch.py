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
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

from sklearn import tree

from scipy import interp

from time import time
from operator import itemgetter
from scipy.stats import randint as sp_randint


from sklearn import svm
from sklearn import cross_validation

from sklearn.metrics import roc_curve, auc, f1_score

from sklearn import tree

from scipy import interp

# Utility function to report best scores
def report(grid_scores, n_top=400):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")  
        
def chunk_arrivals(row):
    # if(row['Cancelled']==1):
        # return -9999
    
    # return int(np.ceil(row['ArrDelay']/15.0))

    if(row['Cancelled']==1):
        return 1
    if(row['ArrDelay']<15):
        return 0
    return 1

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
        
years=sys.argv[1:]

delays=pd.DataFrame()

print 'Reading ...'
for year in years:
    delays=delays.append(pd.read_pickle('../Data/delays_weather_'+str(year)))


jfk_airport_id=12478
sfo_airport_id=14771
ord_airport_id=13930

# AA_airline_id=19805

delays=delays[delays.OriginAirportID == jfk_airport_id]
delays=delays[delays.DestAirportID == ord_airport_id]
# delays=delays[delays.AirlineID == AA_airline_id]

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

delays.to_csv('A.csv')
# delays.loc[:,featurelabels].to_csv('A.csv')

# sys.exit()
# featurelabels.append(['Airlineid'+str(i) for i in range(0,len(vec_airlines[0]))])
X=delays.loc[:,featurelabels].values
X=np.hstack((X,vec_Airlines))
X=np.hstack((X,vec_DayOfWeek))
X=np.hstack((X,vec_Month))
X=np.hstack((X,vec_DayOfMonth))

# X=np.hstack((X,vec_dephours))
# X=np.hstack((X,vec_arrhours))

for i in range(0,len(vec_Airlines[0])):
    featurelabels.append('Airlineid'+str(i))

for i in range(0,len(vec_DayOfWeek[0])):
    featurelabels.append('DayOfWeek'+str(i))
    
for i in range(0,len(vec_Month[0])):
    featurelabels.append('Month'+str(i))
    
for i in range(0,len(vec_DayOfMonth[0])):
    featurelabels.append('DayOfMonth'+str(i))
# for i in range(0,len(vec_dephours[0])):
#     featurelabels.append('DepHour'+str(i))
#
# for i in range(0,len(vec_arrhours[0])):
#     featurelabels.append('ArrHour'+str(i))
# 
print featurelabels
# np.savetxt("A.csv", X, delimiter=",")
# delays.loc[:,featurelabels].to_csv('A.csv')

# sys.exit()

y=delays['ArrDelayGroup'].values

# y.to_csv('B.csv')
# sys.exit()

classifier = GradientBoostingClassifier()

param_dist = {"n_estimators": [50, 100, 200, 400, 800],
              "max_depth": [1,2,4,8,16,32,None],
              "max_features": sp_randint(1, len(featurelabels)),
              "min_samples_split": sp_randint(1, len(featurelabels)),
              "min_samples_leaf": sp_randint(1, len(featurelabels))}
# run randomized search
              # "bootstrap": [True, False],
n_iter_search = 400
random_search = RandomizedSearchCV(classifier, param_distributions=param_dist,
                                   n_iter=n_iter_search)

start = time()
random_search.fit(X, y)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.grid_scores_)