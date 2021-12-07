let theWheel = null;

function setUpWheel () {  

    theWheel = new Winwheel({
    'numSegments'  : 6,     // Specify number of segments.
    'outerRadius'  : 212,   // Set outer radius so wheel fits inside the background.
    'textFontSize' : 28,    // Set font size as desired.
    'segments'     :        // Define segments including colour and text.
    [
    {'fillStyle' : '#ffbdbd', 'text' : 'Computers'},
    {'fillStyle' : '#89f26e', 'text' : 'Animals'},
    {'fillStyle' : '#7de6ef', 'text' : 'Literature'},
    {'fillStyle' : '#e7706f', 'text' : 'Philosophy'},
    {'fillStyle' : '#eae56f', 'text' : 'History'},
    {'fillStyle' : '#b795fc', 'text' : 'Sports'}
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
let stopAt = (angle + Math.floor((Math.random() * 58)))

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



