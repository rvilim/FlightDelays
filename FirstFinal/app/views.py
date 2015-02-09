from flask import Flask,render_template, request,Markup, jsonify, Response
from app import app
from datetime import datetime
import urlparse
import lookups
import urllib, json
from getconnections import getconnections
import pymysql as mdb

@app.route('/')


            
@app.route('/index')
def cities_input():
    return render_template("input2.html")
  
@app.route('/flightinfo')
def flightinfo():
    
    parsed = urlparse.urlparse(request.url)
    urlvars=urlparse.parse_qs(parsed.query)

    fsurl="https://api.flightstats.com/flex/schedules/rest/v1/json/flight/"
    fsurl+= urlvars['flightairline'][0]+"/"
    fsurl+= urlvars['flightnumber'][0]+"/departing/"
    fsurl+= urlvars['flightdate'][0]+"?appId=bd500382&appKey=a43d87e86904446f95123cdac297e934";

    print fsurl
    response = urllib.urlopen(fsurl);
    data = json.loads(response.read())

    returnflights={}
    i=0
    
    print "hi", data['scheduledFlights']
    if (not data['scheduledFlights']):
        returnflights={"Error" : "Flight not found"}
    for scheduledFlight in data['scheduledFlights']:
        
        flight={}
        if ("isCodeshare" =="true"):
            flight["AirlineID"]=lookups.LookupAirline(scheduledFlight["operator"]["carrierFsCode"])[0]
        else:
            flight["AirlineID"]=lookups.LookupAirline(scheduledFlight["carrierFsCode"])[0]
            
        Origin_Airport=lookups.LookupAirport(scheduledFlight["departureAirportFsCode"])
        Dest_Airport=lookups.LookupAirport(scheduledFlight["arrivalAirportFsCode"])

        if((Origin_Airport is None) or (Dest_Airport is None)):
            returnflights={"Error" : "The origin or destination airport was not found"}
            return Response(response=json.dumps(returnflights), status=200, mimetype="text/plain")
            
        flight["DepTime"]=datetime.strftime(\
                                      datetime.strptime(scheduledFlight["departureTime"], '%Y-%m-%dT%H:%M:%S.000')\
                                      , '%m/%d/%Y %I:%M %p')
        
        flight["ArrTime"]=datetime.strftime(\
                                      datetime.strptime(scheduledFlight["arrivalTime"], '%Y-%m-%dT%H:%M:%S.000') \
                                      , '%m/%d/%Y %I:%M %p')
        

        flight["Origin_Airport_ID"]=Origin_Airport[0]
        flight["Dest_Airport_ID"]=Dest_Airport[0]
        flight["Origin_Airport_Code"]=Origin_Airport[1]
        flight["Dest_Airport_Code"]=Dest_Airport[1]
        flight["Origin_Airport_Name"]=Origin_Airport[2]
        flight["Dest_Airport_Name"]=Dest_Airport[2]

        returnflights[i]=flight

        i=i+1
    return Response(response=json.dumps(returnflights), status=200, mimetype="text/plain")# application/json
      
@app.route('/options')
def airports_output():
    con = mdb.connect('localhost', 'root', '', 'flights') #host, user, password, #database
    parsed = urlparse.urlparse(request.url)
    urlvars=urlparse.parse_qs(parsed.query)
    
    html=''
    airports=''
    # if('Origin_Airport_ID' not in urlvars):
    #     with con:
    #         query="select Airport_ID, Airport_Cityname FROM Airports WHERE 1;";
    #         cur = con.cursor()
    #         cur.execute(query)
    #
    #         query_results = cur.fetchall()
    #
    #         airports={}
    #         for result in query_results:
    #             airports[result[0]]=result[1]
    #             # html=html+'<option value="'+str(result[0])+'">'+result[1]+'</option>\n'
    # else if ('Dest_Airport_ID' not in urlvars):
    #     with con:
    #         query="select Airport_ID, Airport_Cityname FROM Airports WHERE Ori;";
    #         cur = con.cursor()
    #         cur.execute(query)
    #
    #         query_results = cur.fetchall()
    #
    #         airports={}
    #         for result in query_results:
    #             airports[result[0]]=result[1]
        
    return jsonify(airports)
    
@app.route('/output')
def cities_output():
  #pull '' from input field and store it
  
  flights=[]
  #
  parsed = urlparse.urlparse(request.url)
  urlvars=urlparse.parse_qs(parsed.query)
  #
  # print urlvars['bycode'][0]
  # if(urlvars['bycode'][0]=="1"):
  #     numlegs=urlvars['numlegs'][0]
  #     print "hi**********"
  #
  #     for i in range(1, int(numlegs)+1):
  #         fsurl="https://api.flightstats.com/flex/schedules/rest/v1/json/flight/"
  #         fsurl+= urlvars['flightairline'+str(i)][0]+"/"
  #         fsurl+= urlvars['flightnumber'+str(i)][0]+"/departing/"
  #         fsurl+= urlvars['flightdate'+str(i)][0]+"?appId=bd500382&appKey=a43d87e86904446f95123cdac297e934";
  #
  #         response = urllib.urlopen(fsurl);
  #         data = json.loads(response.read())
  #
  #         for leg in data["scheduledFlights"]:
  #             print leg
  #     # for i in range(1,(len(urlvars)))
      

  numlegs=urlvars['numlegs'][0]
  for i in range(1,int(numlegs)+1):
      flight={}
      flight["DepTime"]=datetime.strptime(urlvars['flightdeptime'+str(i)][0], '%m/%d/%Y %I:%M %p')
      flight["ArrTime"]=datetime.strptime(urlvars['flightarrtime'+str(i)][0], '%m/%d/%Y %I:%M %p')
      flight["AirlineID"]=urlvars['airline'+str(i)][0]
      flight["Origin_Airport_ID"]=urlvars['originairport'+str(i)][0]
      flight["Dest_Airport_ID"]=urlvars['destairport'+str(i)][0]

      flights.append(flight)

  probabilities = getconnections(flights)
  
  routetext="<div class='col-md-12'><h3>"+probabilities[0]["Airport_Code"]
  ontimetext=""
  
  for i in range(1,len(flights)+1):
      routetext=routetext+"-->"+probabilities[i]['Airport_Code']
       
  routetext=routetext+"</h3></div>" 
  
  greatcircletext="var start = { x: "+str(probabilities[0]["Airport_Longitude"])+" , y: "+str(probabilities[0]["Airport_Latitude"])+" };"
  route=[]
  airport={}
  airport["Airport_Pos"]=[probabilities[0]["Airport_Latitude"],probabilities[0]["Airport_Longitude"]]
  airport["Airport_Cityname"]=probabilities[0]["Airport_Cityname"]
  airport["Airport_Code"]=probabilities[0]["Airport_Code"]
  route.append(airport)
  
  print route
  
  stopovers=[]
  
  for i,probability in enumerate(probabilities):
      if(i==0):
          continue

      
      route.append({"Airport_Pos": [probability["Airport_Latitude"],probability["Airport_Longitude"]], 
                    "Airport_Cityname": probability["Airport_Cityname"], "Airport_Code": probability["Airport_Code"] })
      if(i<len(probabilities)-1):
          stopovers.append({"Airport_Code": probability['Airport_Code'], "Airport_Cityname": probability['Airport_Cityname'],
                            "MinConnect": probability["MinConnect"], "ChanceCatch": probability["ChanceCatch"],
                            "Airport_Pos": [probability["Airport_Latitude"],probability["Airport_Longitude"]]})
                
      if(i==len(probabilities)-1):
          # destination=[probability['Airport_Code'], probability['Airport_Cityname'], probability["ArrivalDelay"], probability ["ArrivalDelayProb"]]
          destination={"Airport_Code": probability['Airport_Code'],  "Airport_Cityname": probability['Airport_Cityname'],
                       "ArrivalDelay": probability["ArrivalDelay"], "ArrivalDelayProb": probability ["ArrivalDelayProb"],
                       "Airport_Pos": [probability["Airport_Latitude"],probability["Airport_Longitude"]]}
      # if(i<len(probabilities)-1):
      #     if(probability["ChanceCatch"]>.5):
      #         ontimetext=ontimetext+"<h3 class=\"text-success\">-You have a connection in "+str(probability['Airport_Cityname'])+", but have "+str(probability["MinConnect"])+ " minutes to connect so we think you'll make it! ({0:.0f}% of success)</h3>".format(100*float(probability["ChanceCatch"]))
      #     else:
      #         print probability
      #         ontimetext=ontimetext+"<h3 \"text-danger\">-You have a tight connection in "+str(probability['Airport_Cityname'])+". You only have "+str(probability["MinConnect"])+ " minutes to connect and might not make it ({0:.0f}% of success)</h3>".format(100*float(probability["ChanceCatch"]))
      #
      #     greatcircletext=greatcircletext+"var start = { x: "+str(probability["Airport_Longitude"])+" , y: "+str(probability["Airport_Latitude"])+" };"
      #
      # if(i>0 and i<len(probabilities)-1):
      #     ontimetext+='<canvas id="myCanvas" width="300px" height="100px"></canvas> \
      #                  <script> \
      #                      var canvas = document.getElementById("myCanvas");\
      #                      var width = canvas.width;\
      #                      var height = canvas.height;\
      #                      var planeimgwidth=30;\
      #                      var planeimgheight=30;\
      #                      var linepadding=5;\
      #                      \
      #                      var canvas = document.getElementById("myCanvas"); \
      #                      var context = canvas.getContext("2d"); \
      #                      var imageObj = new Image(); \
      #                      imageObj.onload = function() { \
      #                          context.drawImage(imageObj, width/2.0-planeimgwidth/2.0, height/2.0-planeimgheight/2.0, planeimgwidth, planeimgheight); \
      #                      }; \
      #                      imageObj.src = "../static/img/airplane.svg"; \
      #                      \
      #                      context.beginPath();\
      #                      context.setLineDash([5]);\
      #                      context.translate(0.5, 0.5);\
      #                      context.moveTo(width/2.0, 0);\
      #                      context.lineTo(width/2.0, (height-2.0*linepadding-planeimgheight)/2.0);\
      #                      context.moveTo(width/2.0, height-(height-2.0*linepadding-planeimgheight)/2.0);\
      #                      context.lineTo(width/2.0, height);\
      #                      context.stroke();\
      #                      </script>'
      #
      #
      # if(i==len(probabilities)-1):
      #     if(probability["ArrivalDelay"]<=15):
      #         ontimetext=ontimetext+"<h3 class=\"text-success\">-You should be on time getting into "+str(probability['Airport_Cityname'])+" ({0:.0f}% confident)</h1>".format(100*float(probability["ArrivalDelayProb"]))
      #     else:
      #         ontimetext=ontimetext+"<h3 \"text-danger\">-You might be late getting into "+str(probability['Airport_Cityname'])+". We estimate you will be about "+str(probability["ArrivalDelay"])+" minutes late ({0:.0f}% confident)</h3>".format(100*float(probability["ArrivalDelayProb"]))
      #
      
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
  return render_template("output.html",route=route, stopovers=stopovers, destination=destination)