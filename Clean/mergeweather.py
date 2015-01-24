import pandas as pd
import numpy as np
import sys
from datetime import datetime

years=sys.argv[1]

weather=pd.DataFrame()
delays=pd.DataFrame()

for year in years:
    weather=weather.append(pd.read_pickle('../Weather/Data/weather_'+str(year)), ignore_index=True)
    delays=delays.append(pd.read_pickle('../Data/delays_'+str(year)), ignore_index=True)

print weather.dtypes