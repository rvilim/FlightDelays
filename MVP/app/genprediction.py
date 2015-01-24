from sklearn.externals import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import holidays
import os

def predict(AirlineID, Airport, flightdatetime):
    print os.getcwd()
    
    forest=joblib.load('app/predicts/dep'+str(Airport))
    
    Year=int(flightdatetime.strftime("%Y"))
    Month=int(flightdatetime.strftime("%m"))
    DayOfWeek=int(flightdatetime.strftime("%w"))
    DayOfMonth= int(flightdatetime.strftime("%d"))
    DayNum=int(flightdatetime.strftime("%j"))
    DepMidnightMinutes=int(flightdatetime.strftime("%H"))*60+int(flightdatetime.strftime("%M"))
    
    shiftingholidays=holidays.getholidays(Year,'NY')
    holidaydeltas=[(flightdatetime.date()-holiday).days for holiday in shiftingholidays]
    DaysToHoliday=holidaydeltas[np.argmin(np.absolute(np.asarray(holidaydeltas)))]
    
    
    indata=[int(AirlineID), Month, DayOfWeek, DayOfMonth, DayNum, DepMidnightMinutes, DaysToHoliday]
    
    output = forest.predict(indata).astype(int)
    prob = forest.predict_proba(indata)
    
    return [output, prob]