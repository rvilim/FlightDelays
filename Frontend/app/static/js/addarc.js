function addarc(startlat, startlon, endlat, endlon, L, map){ 
  start = { x: startlon, y: startlat };  
  end = { x: endlon, y: endlat };

  var generator = new arc.GreatCircle(start, end, { name: 'Seattle to DC' ,'color':'#FF0000' } );
  var line = generator.Arc(400, { offset: 10 });
  L.geoJson(line.json()).addTo(map);

  console.log('HI')
return L
}