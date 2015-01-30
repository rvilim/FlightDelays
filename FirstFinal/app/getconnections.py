from genprediction import predict
import datetime
import numpy as np
import itertools

def peek(iterable):
    peek = iterable.next()
    return peek, itertools.chain([peek], iterable)
    
def getconnections(flights):
    i=0
    
    probabilities=[]
    
    # a=iter(flights)

    minconnect=30    
    
    route=[flights[0]["Origin_Airport_ID"]]
    
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
            print flight["Origin_Airport_ID"],'->',flight["Dest_Airport_ID"]
            print flight["ArrTime"], 'transfer', nextflight["DepTime"]
            # print nextflight["DepTime"], flight["ArrTime"]
            # print contime,  int(contime/15.0)
            for i in range(0,int(contime/15.0)):
                chancecatch=chancecatch+prob[np.where(delayclass==i)]
                # print prob
            probabilities.append([nextflight["Origin_Airport_ID"], minconnect, chancecatch])
            route=route+[flight["Dest_Airport_ID"]]
        else:
            print "Last"
            print flight["Origin_Airport_ID"],'->',flight["Dest_Airport_ID"]
            probabilities.append([flight["Dest_Airport_ID"], 15*delayclass[np.argmax(prob)],np.amax(prob)])
            route=route+[flight["Dest_Airport_ID"]]
            
    return [probabilities,route]
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
