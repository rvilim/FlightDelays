def genconnections(flights):
    i=0
    
    for flight in flights:
        prediction[i]=predict(flight)
        i++
        