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

cv = cross_validation.StratifiedKFold(y, n_folds=10)

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv):

    print 'Training ...'
    classifier = GradientBoostingClassifier(n_estimators=100, max_features=63, min_samples_split=57, max_depth=4, min_samples_leaf=14)

    weights=balance_weights(y[train])

    classifier = classifier.fit( X[train], y[train])#, sample_weight=weights)
    probas_ = classifier.predict_proba(X[test])
    
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
    print f1_score(y[test], classifier.predict(X[test]), average='weighted')


# importances = classifier.feature_importances_
# std = np.std([tree.feature_importances_ for tree in classifier.estimators_],
             # axis=0)
# indices = np.argsort(importances)[::-1]

# Print the feature ranking
# print("Feature ranking:")
# numfeatures=np.shape(indices)[0]

# for f in range(numfeatures):
    # print("%d. feature %d (%f pm %f) - %s" % (f + 1, indices[f], importances[indices[f]], std[indices[f]], featurelabels[f]))

# ROC Curve
plt.plot([0, 1], [0, 1], '--', color=(0.6, 0.6, 0.6), label='Luck')

mean_tpr /= len(cv)
mean_tpr[-1] = 1.0
mean_auc = auc(mean_fpr, mean_tpr)
plt.plot(mean_fpr, mean_tpr, 'k--',
         label='Mean ROC (area = %0.2f)' % mean_auc, lw=2)

plt.xlim([-0.05, 1.05])
plt.ylim([-0.05, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver operating characteristic example')
# plt.legend(loc="lower right")
plt.savefig('roc.pdf',dpi=300)
