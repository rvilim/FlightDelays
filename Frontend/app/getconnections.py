from genprediction import predict
import datetime
import numpy as np
import itertools
import pymysql as mdb


def getairportinfo(Airport_ID):
    
    conn = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
    cur = conn.cursor()

    query="SELECT Airport_ID, Airport_Code, Airport_Cityname, X(Position) , Y(Position) \
           FROM Airports WHERE Airport_ID="+Airport_ID+";"
           
    cur.execute(query)
    info=cur.fetchone()
    
    Airport_Info={}
    Airport_Info["Airport_ID"]=info[0]
    Airport_Info["Airport_Code"]=info[1]
    Airport_Info["Airport_Cityname"]=info[2]
    Airport_Info["Airport_Longitude"]=info[4]
    Airport_Info["Airport_Latitude"]=info[3]
    
    conn.close()
    
    return Airport_Info    
    
def getconnections(flights):
    i=0
    
    probabilities=[]

    # a=iter(flights)

    minconnect=45    
    
    # route=[getairportinfo(flights[0]["Origin_Airport_ID"])]
    probabilities.append(getairportinfo(flights[0]["Origin_Airport_ID"]))
        
    numflights=len(flights)
    
    for i in range(0,numflights):
        flight=flights[i]

        if(i!=(numflights-1)):
            nextflight=flights[i+1]
        else:
            nextflight=None
                    
        [prob, delayclass]=predict(flight)

        if(-1 in delayclass):
            cancelledprob=delayclass.index(-1)
        
        if(nextflight is not None):
            nextdep=nextflight["DepTime"]

            contime=(nextflight["DepTime"]-datetime.timedelta(minutes=minconnect)-flight["ArrTime"]).total_seconds() / 60

            chancecatch=0.0
            # print flight["Origin_Airport_ID"],'->',flight["Dest_Airport_ID"]
            # print flight["ArrTime"], 'transfer', nextflight["DepTime"]
            # print nextflight["DepTime"], flight["ArrTime"]
            # print contime,  int(contime/15.0)
            for i in range(0,int(contime/15.0)):
                probchunk=prob[np.where(delayclass==i)]
                
                if probchunk:
                    chancecatch=chancecatch+probchunk
                    print chancecatch,prob[np.where(delayclass==i)]
            connection=getairportinfo(nextflight["Origin_Airport_ID"])
            connection["MinConnect"]=minconnect
            connection["ArrivalDelay"]=15*delayclass[np.argmax(prob)]
            connection["ChanceCatch"]=chancecatch
            print chancecatch, prob, delayclass
            probabilities.append(connection)
            # route=route+[getairportinfo(flight["Dest_Airport_ID"])]
        else:
            # print "Last"
            # print flight["Origin_Airport_ID"],'->',flight["Dest_Airport_ID"]
            destination=getairportinfo(flight["Dest_Airport_ID"])
            destination["ArrivalDelay"]=15*delayclass[np.argmax(prob)]
            # print np.amax(prob)
            destination["ArrivalDelayProb"]=np.amax(prob)
            probabilities.append(destination)
            # route=route+[getairportinfo(flight["Dest_Airport_ID"])]
            
    return probabilities
    # for nextflight in a:
    #     if(i==0):
    #         flight=nextflight
    #         i=i+1
    #     else:
    #         # Get the probability of the flight arriving late
    #         #
    #         # print prob
    #         # print delayclass
    #
    #         # If the flight might be cancelled, get the probability of that.

    #         i=i+1
