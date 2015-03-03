from sklearn.externals import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
import holidays
import os
from getweather import getforecast
from sklearn.preprocessing import OneHotEncoder

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
    Airline_ID=flight["AirlineID"]
    DepTime=flight["DepTime"]
    ArrTime=flight["ArrTime"]
    
    classifier=joblib.load('app/classifiers/'+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))

    Airlinesenc = joblib.load("app/vectorizers/Airlinesenc_"+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))
    DayOfWeekenc = joblib.load("app/vectorizers/DayOfWeekenc_"+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))
    Monthenc = joblib.load("app/vectorizers/Monthenc_"+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))
    DayOfMonthenc = joblib.load("app/vectorizers/DayOfMonthenc_"+str(Origin_Airport_ID)+'->'+str(Dest_Airport_ID))

    [Weather_Origin_prev, Weather_Origin]=getforecast(DepTime, Origin_Airport_ID)
    [Weather_Dest_prev, Weather_Dest]=getforecast(ArrTime, Dest_Airport_ID)

    DepMidnightHours=int(DepTime.strftime("%H"))
    ArrMidnightHours=int(ArrTime.strftime("%H"))
    
    DaysToHoliday=distancetoholiday(DepTime)

    Month=int(DepTime.strftime("%m"))
    DayOfWeek=int(DepTime.strftime("%w"))
    DayOfMonth= int(DepTime.strftime("%d"))

    vec_Airlines=get_vectorized([Airline_ID],Airlinesenc)
    vec_DayOfWeek=get_vectorized([DayOfWeek],DayOfWeekenc)
    vec_Month=get_vectorized([Month],Monthenc)
    vec_DayOfMonth=get_vectorized([DayOfMonth],DayOfMonthenc)
    
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

    indata = [ DepMidnightHours, ArrMidnightHours, DaysToHoliday,
               Prcp_Dest,Snow_Dest,AWnd_Dest,WSf2_Dest,WDf2_Dest,
               Prcp_Dest_prev,Snow_Dest_prev,AWnd_Dest_prev,WSf2_Dest_prev,WDf2_Dest_prev,
               Prcp_Origin,Snow_Origin,AWnd_Origin,WSf2_Origin,WDf2_Origin,
               Prcp_Origin_prev,Snow_Origin_prev,AWnd_Origin_prev,WSf2_Origin_prev,WDf2_Origin_prev
              ]
    
    indata=indata+vec_Airlines[0].tolist()+vec_DayOfWeek[0].tolist()+vec_Month[0].tolist()+vec_DayOfMonth[0].tolist()

    # print indata
    output = classifier.predict(indata).astype(int)
    prob = classifier.predict_proba(indata)
    # print "Output: "+str(output)+" "+str(probs[0])
    # print '---------'
    # print classifier.classes_
    # print '---------'
    # print probs
    # for prob, delayclass in zip(classifier.classes_, probs[0]):
    #     print prob, delayclass
    
    return [prob[0], classifier.classes_]