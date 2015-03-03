import matplotlib
import pandas as pd
import numpy as np
import sys

import matplotlib.pyplot as plt
from datetime import datetime

years=sys.argv[1:]

delays=pd.DataFrame()

print 'Reading ...'
for year in years:
    delays=delays.append(pd.read_pickle('../../Data/delays_'+str(year)))

jfk_airport_id=12478
sfo_airport_id=14771
ohare_airport_id=13930

delays=delays[delays.DestAirportID == sfo_airport_id]
# delays=delays[delays.OriginAirportID == jfk_airport_id]
# delays=delays[delays.AirlineID == AA_airline_id]

delays=delays[(delays['Cancelled']==0)&(delays['Diverted']==0)]

num_bins=30
bins = [-60,-45,-30,-15,0,15,30,45,60,75,90,105,120,135,150,165,180,195,210]

n, bins, patches = plt.hist(delays['ArrDelay'].values, bins, normed=1, facecolor='grey', alpha=0.5,cumulative=True)
# Tweak spacing to prevent clipping of ylabel
plt.xlabel('Minutes late')
plt.ylabel('Normalized Histogram')
plt.ylim([0, 1])
plt.title('Arriving at SFO '+str(min(map(int,years)))+'-'+str(max(map(int,years))))
plt.subplots_adjust(left=0.15)
plt.savefig('SFO_cum_2010-2014.eps')