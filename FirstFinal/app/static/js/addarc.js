function addarc(startlat, startlon, endlat, endlon, L, map){ 
  start = { x: startlon, y: startlat };  
  end = { x: endlon, y: endlat };

  var generator = new arc.GreatCircle(start, end, { name: 'Seattle to DC' });
  var line = generator.Arc(100, { offset: 10 });
  L.geoJson(line.json()).addTo(map);

return L
}