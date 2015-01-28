from flask import render_template, request,Markup
from app import app
import pymysql as mdb
from datetime import datetime
from genprediction import predict
db = mdb.connect(user="root", host="localhost", db="world_innodb", charset='utf8')

@app.route('/')
    
@app.route('/index')
def cities_input():
    return render_template("input.html")
    

@app.route('/output')
def cities_output():
  #pull '' from input field and store it
  airline=request.args.get('airline')
  airport=request.args.get('airport')
  flightdatetime=datetime.strptime(request.args.get('flightdatetime'), '%m/%d/%Y %I:%M %p')

  [output, prob]= predict(airline, airport, flightdatetime)
  
  print output, prob
  
  if (output==1):
      delayed="<h1 class=\"text-danger\">Your flight is likely going to be delayed ({0:.0f}%)".format(100*float(prob[0][0]))+"</h1>"
  else:
      delayed="<h1 class=\"text-success\">Your flight will probably be on time ({0:.0f}%)".format(100*float(prob[0][0]))+"</h1>"
      
  return render_template("output.html", airline=airline, airport=airport, flightdatetime=flightdatetime, delayed=delayed )