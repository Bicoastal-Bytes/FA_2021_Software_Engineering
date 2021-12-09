let theWheel = null;
let arr = new Array(6);
let catArray = ['Animals', 'Entertainment: Film', 'History', 'Celebrities', 'Geography', 'Entertainment: Books'];

function setUpWheel () {  

    fetch('/api/wheel')
    .then(resp => resp.json())
    .then(function(data) {
        arr = data.categories;
    })

    for (var i = 0; i < arr.length; i++){
        //document.write("<br><br>array index: " + i);
        var obj = arr[i];
        for (var key in obj){
          var value = obj[key];
          if (key == 'name') {
            //document.write("<br> - " + key + ": " + value);
            catArray[i] = value;
            }
        }
      }


    theWheel = new Winwheel({
    'numSegments'  : 6,     // Specify number of segments.
    'outerRadius'  : 212,   // Set outer radius so wheel fits inside the background.
    'textFontSize' : 14,    // Set font size as desired.
    'segments'     :        // Define segments including colour and text.
    [
    {'fillStyle' : '#ffbdbd', 'text' : catArray[0]},
    {'fillStyle' : '#89f26e', 'text' : catArray[1]},
    {'fillStyle' : '#7de6ef', 'text' : catArray[2]},
    {'fillStyle' : '#e7706f', 'text' : catArray[3]},
    {'fillStyle' : '#eae56f', 'text' : catArray[4]},
    {'fillStyle' : '#b795fc', 'text' : catArray[5]}
    ],
    'animation' :
    {
        'type'          : 'spinToStop',
        'duration'      : 5,
        'spins'         : 8,
        'callbackAfter' : 'drawTriangle()'
    }
    });

}



// Function with formula to work out stopAngle before spinning animation.
// Called from Click of the Spin button.
function calculatePrize(angle, cats = null)
{

 console.log('angle: ' + angle);
    
/* initialize the wheel each turn */
setUpWheel();

// This formula always makes the wheel stop somewhere inside prize 3 at least
// 1 degree away from the start and end edges of the segment.
let stopAt = angle;

// Important thing is to set the stopAngle of the animation before stating the spin.
theWheel.animation.stopAngle = stopAt;

// May as well start the spin from here.
theWheel.startAnimation();

// forward to the point value page after wheel has spun
setTimeout(() => {
        turnOn('pointvalue');
    }, 7000);   
}

// Usual pointer drawing code.
drawTriangle();

function drawTriangle()
{
// Get the canvas context the wheel uses.
let ctx = theWheel.ctx;

ctx.strokeStyle = 'navy';     // Set line colour.
ctx.fillStyle   = 'aqua';     // Set fill colour.
ctx.lineWidth   = 2;
ctx.beginPath();              // Begin path.
ctx.moveTo(180, 5);           // Move to initial position.
ctx.lineTo(240, 5);           // Draw lines to make the shape.
ctx.lineTo(210, 40);
ctx.lineTo(180, 5);
ctx.stroke();                 // Complete the path by stroking (draw lines).
ctx.fill();                   // Then fill.
}



