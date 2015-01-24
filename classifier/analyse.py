import matplotlib

matplotlib.use('Agg')


import pandas as pd
import numpy as np
import csv as csv
import sys

import matplotlib.pyplot as plt
from datetime import datetime
from random import sample

from sklearn.ensemble import ExtraTreesClassifier
from sklearn import svm
from sklearn import cross_validation

from sklearn.metrics import roc_curve, auc, f1_score

from sklearn import tree

from scipy import interp

years=sys.argv[1:]

delays=pd.DataFrame()

print 'Reading ...'
for year in years:
    delays=delays.append(pd.read_pickle('Data/delays_'+str(year)))

jfk_airport_id=12478
# AA_airline_id=19805

delays=delays[delays.OriginAirportID == jfk_airport_id]
# delays=delays[delays.AirlineID == AA_airline_id]

delays=delays[(delays['Cancelled']==0)&(delays['Diverted']==0)]


delays['DaysToHoliday']=delays['DaysToHoliday'].apply(lambda x: x if np.abs(x)<4 else 1000)
delays['DepMidnightMinutes']=delays['DepMidnightMinutes'].apply(lambda x: x - x % 60)
print delays

featurelabels=['AirlineID','Month', 'DayOfWeek', 'DayOfMonth', 'DayNum', 'DepMidnightMinutes', 'DaysToHoliday']


X=delays.loc[:,featurelabels].values
y=delays['DepDelayed'].values

print X

cv = cross_validation.StratifiedKFold(y, n_folds=10)

mean_tpr = 0.0
mean_fpr = np.linspace(0, 1, 100)
all_tpr = []

for i, (train, test) in enumerate(cv):

    print 'Training ...'
    classifier = ExtraTreesClassifier(n_estimators=250, n_jobs=-1)
    
    classifier = classifier.fit( X[train], y[train])
    probas_ = classifier.predict_proba(X[test])
    
    fpr, tpr, thresholds = roc_curve(y[test], probas_[:, 1])
    mean_tpr += interp(mean_fpr, fpr, tpr)
    mean_tpr[0] = 0.0
    roc_auc = auc(fpr, tpr)
    # plt.plot(fpr, tpr, lw=1, label='ROC fold %d (area = %0.2f)' % (i, roc_auc))
    # print f1_score(y[test], classifier.predict(X[test]), average='weighted')


importances = classifier.feature_importances_
std = np.std([tree.feature_importances_ for tree in classifier.estimators_],
             axis=0)
indices = np.argsort(importances)[::-1]

# Print the feature ranking
print("Feature ranking:")
numfeatures=np.shape(indices)[0]

for f in range(numfeatures):
    print("%d. feature %d (%f pm %f) - %s" % (f + 1, indices[f], importances[indices[f]], std[indices[f]], featurelabels[f]))

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