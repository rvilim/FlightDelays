from sklearn.externals import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import holidays
import os

def get_vectorized(catarray, enc):
    catarray=[[i] for i in catarray]
    return enc.transform(catarray).toarray()

def distancetoholiday(DepTime):

    daysoff=holidays.getholidays(DepTime.year,"NY")
    # This does a list comprehension to get the distance from each holiday
    holidaydeltas=[(DepTime.date()-holiday).days for holiday in daysoff]

    # This then converts that to a numpy array
    # then takes the absolute value of all the variables in that numpy array, then gets the location of the closest
    # and finally returns the number of days to the closest holiday. Whew!    
    return holidaydeltas[np.argmin(np.absolute(np.asarray(holidaydeltas)))]
    
def predict(flight):
    Origin_Airport_ID=flight["Origin_Airport_ID"]
    Dest_Airport_ID=flight["Dest_Airport_ID"]
    AirlineID=flight["AirlineID"]
    DepTime=flight["DepTime"]
    ArrTime=flight["ArrTime"]
    
    forest=joblib.load('app/predicts/'+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))

    Airlinesenc = joblib.load("vectorizers/Airlinesenc_"+str(origin_airport_id)+'->'+str(dest_airport_id)) 
    DayOfWeekenc = joblib.load("vectorizers/DayOfWeekenc_"+str(origin_airport_id)+'->'+str(dest_airport_id)) 
    MonthEnc = joblib.load("vectorizers/MonthEnc_"+str(origin_airport_id)+'->'+str(dest_airport_id)) 
    DayOfMonthEnc = joblib.load("vectorizers/DayOfMonthEnc_"+str(origin_airport_id)+'->'+str(dest_airport_id)) 

    [Weather_Origin_prev, Weather_Origin]=getforecast(DepTime, Origin_Airport_ID)
    [Weather_Dest_prev, Weather_Dest]=getforecast(ArrTime, Dest_Airport_ID)

    DepMidnightHours=int(DepTime.strftime("%H"))
    ArrMidnightHours=int(ArrTime.strftime("%H"))
    
    DaysToHoliday=distancetoholiday(DepTime)

    Prcp_Dest=Weather_Dest["PRCP"]
    Snow_Dest=Weather_Dest["SNOW"]
    AWnd_Dest=Weather_Dest["AWND"]
    WSf2_Dest=Weather_Dest["WSF2"]
    WDf2_Dest=Weather_Dest["WDF2"]

    Prcp_Dest_prev=Weather_Dest_prev["PRCP"]
    Snow_Dest_prev=Weather_Dest_prev["SNOW"]
    AWnd_Dest_prev=Weather_Dest_prev["AWND"]
    WSf2_Dest_prev=Weather_Dest_prev["WSF2"]
    WDf2_Dest_prev=Weather_Dest_prev["WDF2"]

    Prcp_Origin=Weather_Origin["PRCP"]
    Snow_Origin=Weather_Origin["SNOW"]
    AWnd_Origin=Weather_Origin["AWND"]
    WSf2_Origin=Weather_Origin["WSF2"]
    WDf2_Origin=Weather_Origin["WDF2"]

    Prcp_Origin_prev=Weather_Origin_prev["PRCP"]
    Snow_Origin_prev=Weather_Origin_prev["SNOW"]
    AWnd_Origin_prev=Weather_Origin_prev["AWND"]
    WSf2_Origin_prev=Weather_Origin_prev["WSF2"]
    WDf2_Origin_prev=Weather_Origin_prev["WDF2"]
       
    
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