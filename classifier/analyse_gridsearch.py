import matplotlib

matplotlib.use('Agg')


import pandas as pd
import numpy as np
import csv as csv
import sys

import matplotlib.pyplot as plt
from datetime import datetime
from random import sample

from sklearn.ensemble import RandomForestClassifier
from sklearn.grid_search import GridSearchCV, RandomizedSearchCV

from sklearn import svm
from sklearn import cross_validation

from sklearn.metrics import roc_curve, auc, f1_score

from sklearn import tree

from scipy import interp

from time import time
from operator import itemgetter
from scipy.stats import randint as sp_randint


    
def chunk_arrivals(row):
    # if(row['Cancelled']==1):
        # return -9999
    
    # return int(np.ceil(row['ArrDelay']/15.0))

    if(row['Cancelled']==1):
        return 1
    if(row['ArrDelay']<15):
        return 0
    return 1

# Utility function to report best scores
def report(grid_scores, n_top=3):
    top_scores = sorted(grid_scores, key=itemgetter(1), reverse=True)[:n_top]
    for i, score in enumerate(top_scores):
        print("Model with rank: {0}".format(i + 1))
        print("Mean validation score: {0:.3f} (std: {1:.3f})".format(
              score.mean_validation_score,
              np.std(score.cv_validation_scores)))
        print("Parameters: {0}".format(score.parameters))
        print("")    
    
years=sys.argv[1:]

delays=pd.DataFrame()

print 'Reading ...'
for year in years:
    delays=delays.append(pd.read_pickle('../Data/delays_weather_'+str(year)))

jfk_airport_id=12478
sfo_airport_id=14771
ord_airport_id=13930

delays=delays[delays.OriginAirportID == jfk_airport_id]
delays=delays[delays.DestAirportID == ord_airport_id]

delays=delays[(delays['Diverted']==0)]

delays['ArrDelayGroup']=delays.apply(chunk_arrivals, axis=1)


featurelabels=['AirlineID','Month', 'DayOfWeek', 'DayOfMonth', 'DayNum', 'DepMidnightMinutes', 'DaysToHoliday',
               'TMax_Dest','TMin_Dest','Prcp_Dest','Snow_Dest','AWnd_Dest','WSf2_Dest','WDf2_Dest',
               'TMax_Dest_prev','TMin_Dest_prev','Prcp_Dest_prev','Snow_Dest_prev','AWnd_Dest_prev','WSf2_Dest_prev','WDf2_Dest_prev',
               'TMax_Origin','TMin_Origin','Prcp_Origin','Snow_Origin','AWnd_Origin','WSf2_Origin','WDf2_Origin',
               'TMax_Origin_prev','TMin_Origin_prev','Prcp_Origin_prev','Snow_Origin_prev','AWnd_Origin_prev','WSf2_Origin_prev','WDf2_Origin_prev'
              ]
featurelabels
X=delays.loc[:,featurelabels].values
y=delays['ArrDelayGroup'].values

clf = RandomForestClassifier(n_estimators=500, n_jobs=-1)
# specify parameters and distributions to sample from


param_dist = {"max_depth": [10, None],
              "max_features": sp_randint(1, len(featurelabels)),
              "min_samples_split": sp_randint(1, len(featurelabels)),
              "min_samples_leaf": sp_randint(1, len(featurelabels)),
              "bootstrap": [True, False],
              "criterion": ["gini", "entropy"]}
# run randomized search
n_iter_search = 40
random_search = RandomizedSearchCV(clf, param_distributions=param_dist,
                                   n_iter=n_iter_search)

start = time()
random_search.fit(X, y)
print("RandomizedSearchCV took %.2f seconds for %d candidates"
      " parameter settings." % ((time() - start), n_iter_search))
report(random_search.grid_scores_)