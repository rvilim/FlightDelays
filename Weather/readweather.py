import pandas as pd
import numpy as np
import csv as csv
import sys

years=sys.argv[1:]

weather=pd.DataFrame()

for year in years:    
    delays=pd.read_csv(str(year)+'.csv')