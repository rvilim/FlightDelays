function addflightspacer(canvasid){ 
  console.log(canvasid);
  var canvas = document.getElementById(canvasid);
  var width = canvas.width;
  var height = canvas.height;
  var planeimgwidth=30;
  var planeimgheight=30;
  var linepadding=5;
  

  var context = canvas.getContext("2d"); 
  context.globalAlpha = 0.5
  
  var imageObj = new Image(); 
  imageObj.onload = function() { 
      context.drawImage(imageObj, width/2.0-planeimgwidth/2.0, height/2.0-planeimgheight/2.0, planeimgwidth, planeimgheight); 
  }; 
  imageObj.src = "../static/img/airplane.svg"; 

  context.beginPath();
  context.setLineDash([1,2]);
  context.translate(0.5, 0.5);
  context.moveTo(width/2.0, 0);
  context.lineTo(width/2.0, (height-2.0*linepadding-planeimgheight)/2.0);
  context.moveTo(width/2.0, height-(height-2.0*linepadding-planeimgheight)/2.0);
  context.lineTo(width/2.0, height);
  context.stroke();
}