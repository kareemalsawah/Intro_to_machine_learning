/*
Fill a canvas with a color.
Arguments:
canvas: Object reference
ctx: the context of the canvas
color: the color to fill the canvas
*/
function drawBackground(canvas,ctx,color){
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.rect(0,0,canvas.width,canvas.height);
  ctx.fill();
  ctx.closePath();
}

/*
Draw a border on a canvas and fill the rest of the canvas with white background
Arguments:
canvas: Object reference
ctx: the context of the canvas
color: the color of the border
width: the width of the border measured in pixels
*/
function drawBorder(canvas,ctx,color,width){
  drawBackground(canvas,ctx,color);
  ctx.beginPath();
  ctx.fillStyle = "white";
  ctx.rect(width,width,canvas.width-2*width,canvas.height-2*width);
  ctx.fill();
  ctx.closePath();
}


/*
Draw x and y axes on the canvas.
Arguments (all measured in canvas pixels):
ctx: the context of the canvas to draw on
x: the x location of the origin of the axes
y: the y location of the origin of the axes
width: the total length of the x-axis (both the positive and negative parts)
height: the total length of the y-axis (both the positive and negative parts)
thickness: the width of both x and y axes
*/
function drawAxes(ctx,x,y,color,width,height,thickness){
  //Draw the x-axis
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.rect(x-width/2,y,width,thickness);
  ctx.fill();
  ctx.closePath();

  //Draw the y-axis
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.rect(x,y-height/2,thickness,height);
  ctx.fill();
  ctx.closePath();
}

/*
Draw a point in a certain color.
Arguments (all measured in canvas pixels):
ctx: the context of the canvas to draw on
x: the x location of the point
y: the y location of the point
color: the color of the point
radius: the radius to draw the point with
*/
function drawPoint(ctx,x,y,color,radius){
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.arc(x, y, radius, 0, 2 * Math.PI);
  ctx.fill();
  ctx.closePath();
}

/*
Draw a rectancle in a certain color.
Arguments (all measured in canvas pixels):
ctx: the context of the canvas to draw on
x: the x location of the top left corner of the rectangle
y: the y location of the top left corner of the rectangle
width: the width of the rectangle
height: the height of the rectangle
color: the color of the rectangle
*/
function drawRect(ctx,x,y,width,height,color){
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.rect(x, y, width,height);
  ctx.fill();
  ctx.closePath();
}

/*
Draw the vertical line that divides the canvas into 2 equal parts.
Arguments:
canvas: Object reference
ctx: the context of the canvas
color: the color of the line
width: the width of the line measured in pixels
*/
function drawMiddleSeperator(canvas,ctx,color,width){
  ctx.beginPath();
  ctx.fillStyle = color;
  ctx.rect(canvas.width/2 - width/2,0,width,canvas.height);
  ctx.fill();
  ctx.closePath();
}

/*
Draw points from an array
Arguments:
ctx: the context of the canvas to draw on
points_arr: an array containing point location (each is an array with 2 elements, the x location and y location)
color: the color of the point
radius: the radius to draw the point with
*/
function drawPoints(ctx,points_arr,color,radius){
  for(var i = 0; i < points_arr.length; i++){
    drawPoint(ctx,points_arr[i][0],points_arr[i][1],color,radius);
  }
}



/*
Draw a line given its parameters
Arguments:
canvas: Object reference
ctx: the context of the canvas
params: the parameters to use to draw the line. params[0] represents the slope, params[1] represents the y-intercept.(Both are measured in local canvas coordinates "y axis increases down and the origin is in the top but passes through the drawn y-axis")
color: the color of the line
width: the width of the line measured in pixels
*/
function drawLine(canvas,ctx,params,color,width){
  var slope = -1*params[0];
  var intercept = canvas.height/2 - params[1];
  ctx.beginPath();
  ctx.moveTo(0, intercept-slope*250);
  ctx.lineTo(500, intercept+slope*250);
  ctx.strokeStyle = color;
  ctx.lineWidth = width;
  ctx.stroke();
  ctx.closePath();
}
