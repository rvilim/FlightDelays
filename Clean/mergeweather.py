import pandas as pd
import numpy as np
import sys
from datetime import datetime

year=sys.argv[1]

weather=pd.DataFrame()
weather=pd.read_pickle('../Weather/Data/weather_'+str(year))

print weather
