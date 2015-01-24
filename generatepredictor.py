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
from sklearn import svm
from sklearn import cross_validation

from sklearn.metrics import roc_curve, auc, f1_score

from sklearn import tree

from scipy import interp

import cPickle as pickle

years=sys.argv[1:]

delays=pd.DataFrame()

print 'Reading ...'
for year in years:
    delays=delays.append(pd.read_pickle('Data/delays_'+str(year)))

jfk_airport_id=12478
delays=delays[delays.OriginAirportID == jfk_airport_id]
delays=delays[(delays['Cancelled']==0)&(delays['Diverted']==0)]

featurelabels=['AirlineID', 'Month', 'DayOfWeek', 'DayOfMonth', 'DayNum', 'DepMidnightMinutes', 'DaysToHoliday']
X=delays.loc[:,featurelabels].values
y=delays['DepDelayed'].values

classifier = RandomForestClassifier(n_estimators=250, n_jobs=-1)
classifier = classifier.fit( X, y)

fileObject = open('dep'+str(jfk_airport_id),'wb')
pickle.dump(classifier,fileObject)
fileObject.close()