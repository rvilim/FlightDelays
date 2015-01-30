from flask import render_template, request,Markup
from app import app
import pymysql as mdb
from datetime import datetime
import urlparse
from getconnections import getconnections

@app.route('/')
    
@app.route('/index')
def cities_input():
    return render_template("input.html")
    

@app.route('/output')
def cities_output():
  #pull '' from input field and store it
  
  flights=[]
  
  parsed = urlparse.urlparse(request.url)
  urlvars=urlparse.parse_qs(parsed.query)
  for i in range(1,(len(urlvars)/4+1)):
      request.args.get('flightdatetime')
      flight={}
      flight["DepTime"]=datetime.strptime(urlvars['flightdeptime'+str(i)][0], '%m/%d/%Y %I:%M %p')
      flight["ArrTime"]=datetime.strptime(urlvars['flightarrtime'+str(i)][0], '%m/%d/%Y %I:%M %p')
      flight["AirlineID"]=urlvars['airline'+str(i)][0]
      flight["Origin_Airport_ID"]=urlvars['originairport'+str(i)][0]
      flight["Dest_Airport_ID"]=urlvars['destairport'+str(i)][0]

      flights.append(flight)

  [probabilities, route] = getconnections(flights)
  
  # if len(flights)>6:
  #     print "Oh fuck"
  # else
  #     colclass=12/len(route)
  #
  #             routetext=routetext++str(probability[0])+"</div>"

  routetext="<div class='col-md-12'><h1>"+flights[0]["Origin_Airport_ID"]
  ontimetext=""
  
  for i in range(0,len(flights)):
      routetext=routetext+"-------->"+flights[i]['Dest_Airport_ID']
      # routetext=routetext+"<div class=\"col-md-3\"><h1><hr style=\"padding-top=20px; background:#F87431; border:0; height:7px\" /></h1></div><div class=\"col-md-2\" ><h1>"+flights[i]['Dest_Airport_ID']+"</h1></div>"
        # routetext=routetext+flights[i]['Dest_Airport_ID']
       
  routetext=routetext+"</h1></div>" 
  for i,probability in enumerate(probabilities):
      print i, len(probabilities)
      if(i<len(probabilities)-1):
          if(probability[2]>.5):
              ontimetext=ontimetext+"<h1 class=\"text-success\">You have a connection in "+str(probability[0])+", but have "+str(probability[1])+ " minutes to connect so we think you'll make it! ({0:.0f}% of success)</h1>".format(100*float(probability[2]))
          else:
              ontimetext=ontimetext+"<h1 \"text-danger\">You have a tight connection in "+probability[0]+". You only have "+probability[1]+ " minutes to connect and might not make it ({0:.0f}% of success)</h1>".format(100*float(probability[2]))
      if(i==len(probabilities)-1):
          if(probability[2]<=15):
              ontimetext=ontimetext+"<h1 class=\"text-success\">You should be on time getting into "+probability[0]+" ({0:.0f}% confident)</h1>".format(100*probability[2])
          else:
              ontimetext=ontimetext+"<h1 \"text-danger\">You might be late getting into "+probability[0]+". We estimate you will be about "+probability[1]+" minutes late ({0:.0f}% confident)</h1>".format(100*probability[2])
          
      
  # airline=request.args.get('airline')
  # airport=request.args.get('airport')
  # flightdatetime=
  #
  # [output, prob]= predict(airline, airport, flightdatetime)
  #
  # print output, prob
  #
  # if (output==1):
  #     delayed="<h1 class=\"text-danger\">Your flight is likely going to be delayed ({0:.0f}%)".format(100*float(prob[0][0]))+"</h1>"
  # else:
  #     delayed="<h1 class=\"text-success\">Your flight will probably be on time ({0:.0f}%)".format(100*float(prob[0][0]))+"</h1>"
   # , airline=airline1, airport=airport1, flightdatetime=flightdatetime1, delayed=delayed 
  return render_template("output.html",ontimetext=ontimetext, routetext=routetext)