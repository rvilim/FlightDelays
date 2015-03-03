function styleairport(lat,lon,late){
  airport=L.circleMarker(L.latLng(lat, lon))
                       .setStyle({ weight: 1, opacity: 0.3, fillOpacity: 1.0})
                       .setRadius(7);

                       if(late==-1){
                         airport.setStyle({Color:"#323333"})
                         airport.setStyle({fillColor:"#323333"})
                       }
                       if(late==0){
                         airport.setStyle({Color:"#9EBF6D"})
                         airport.setStyle({fillColor:"#9EBF6D"})
                       }
                       if(late==1){
                         airport.setStyle({Color:"#FA6C61"})
                         airport.setStyle({fillColor:"#FA6C61"})
                       }
  return airport
}