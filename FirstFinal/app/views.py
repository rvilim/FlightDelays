from flask import render_template, request,Markup
from app import app
import pymysql as mdb
from datetime import datetime
import urlparse
from genprediction import predict

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

  genconnections(flights)
      
  print flights
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
  return render_template("output.html")