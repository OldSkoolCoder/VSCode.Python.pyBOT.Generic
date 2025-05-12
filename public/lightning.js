// if you just don't want to read the code but still are interested in how it works, here's a guide for you: https://codepen.io/towc/blog/a-guide-to-wavy-waved-radial-waves/

    var w = lightning_canvas.width = window.innerWidth,
		h = lightning_canvas.height = window.innerHeight,
		ctx = lightning_canvas.getContext('2d'),

		opts = {

			rays: 30,
			maxRadius: Math.sqrt( w*w/4 + h*h/4 ),
			circleRadiusIncrementAcceleration: 2,
			radiantSpan: 0.4,
			rayAngularVelSpan: 0.005,
			rayAngularVelLineWidthMultiplier: 60,
			rayAngularAccWaveInputBaseIncrementer: .03,
			rayAngularAccWaveInputAddedIncrementer: .02,
			rayAngularAccWaveMultiplier: .0003,
			baseWaveInputIncrementer: .01,
			addedWaveInputIncrementer: .01,
			circleNumWaveIncrementerMultiplier: .1,
			
			cx: w / 2,
			cy: h / 2,
			tickHueMultiplier: 6,
			shadowBlur: 0,
			repaintAlpha: 0.20,//.2,
			apply: init
		},
		
		rays = [],
		tick2 = 0,
		tickHueMultiplied

function init(){
	
	rays.length = 0;
	for( var i = 0; i < opts.rays; ++i )
		rays.push( new Ray );
	
    loop();
}

function loop(){
	
	window.requestAnimationFrame( loop );
	
  ++tick2;
	
  if (lightning_canvas.classList.contains('invisible') == false){
    console.log('Lightning Running');
	ctx.globalCompositeOperation = 'source-over';
	ctx.shadowBlur = 0;
	ctx.fillStyle = 'rgba(0,0,0,alp)'.replace( 'alp', opts.repaintAlpha );
	ctx.fillRect( 0, 0, w, h );
	ctx.shadowBlur = opts.shadowBlur;
	ctx.globalCompositeOperation = 'lighter';
	
	tickHueMultiplied = opts.tickHueMultiplier * tick2;
	
	rays.map( function( ray ){ ray.step(); } );
  }
}

function Ray(){
	
	this.circles = [ new Circle( 0 ) ];
	this.rot = Math.random() * Math.PI * 2;
	this.angularVel = Math.random() * opts.rayAngularVelSpan * ( Math.random() < .5 ? 1 : -1 );
	this.angularAccWaveInput = Math.random() * Math.PI * 2;
	this.angularAccWaveInputIncrementer = opts.rayAngularAccWaveInputBaseIncrementer + opts.rayAngularAccWaveInputAddedIncrementer * Math.random();
	
	var security = 100,
			count = 0;
	
	while( --security > 0 && this.circles[ count ].radius < opts.maxRadius )
		this.circles.push( new Circle( ++count ) );
}
Ray.prototype.step = function(){
	
	// this is just messy, but if you take your time to read it properly you'll understand it pretty easily
	this.rot += 
		this.angularVel += Math.sin( 
			this.angularAccWaveInput += 
				this.angularAccWaveInputIncrementer ) * opts.rayAngularAccWaveMultiplier;
	
	var rot = this.rot,
			x = opts.cx,
			y = opts.cy;
	
	ctx.lineWidth = Math.min( .00001 / Math.abs( this.angularVel ), 10 / opts.rayAngularVelLineWidthMultiplier ) * opts.rayAngularVelLineWidthMultiplier;

	ctx.beginPath();
	ctx.moveTo( x, y );
	
	for( var i = 0; i < this.circles.length; ++i ){
		
		var circle = this.circles[ i ];
		
		circle.step();
		
		rot += circle.radiant;
		
		var x2 = opts.cx + Math.sin( rot ) * circle.radius,
				y2 = opts.cy + Math.cos( rot ) * circle.radius,
				
				mx = ( x + x2 ) / 2,
				my = ( y + y2 ) / 2;
		
		ctx.quadraticCurveTo( x, y, mx, my );
		
		x = x2;
		y = y2;
	}
	
	ctx.strokeStyle = ctx.shadowColor = 'hsl(hue,80%,50%)'.replace( 'hue', ( ( ( rot + this.rot ) / 2 ) % ( Math.PI * 2 ) ) / Math.PI * 30 + tickHueMultiplied );
	
	ctx.stroke();
}

function Circle( n ){
	
	this.radius = opts.circleRadiusIncrementAcceleration * Math.pow( n, 2 );
	this.waveInputIncrementer = ( opts.baseWaveInputIncrementer + opts.addedWaveInputIncrementer * Math.random() ) * ( Math.random() < .5 ? 1 : -1 ) * opts.circleNumWaveIncrementerMultiplier * n;
	this.waveInput = Math.random() * Math.PI * 2;
	this.radiant = Math.random() * opts.radiantSpan * ( Math.random() < .5 ? 1 : -1 );
}
Circle.prototype.step = function(){
	
	this.waveInput += this.waveInputIncrementer;
	this.radiant = Math.sin( this.waveInput ) * opts.radiantSpan;
}
init();

window.addEventListener( 'resize', function(){
	
	w = lightning_canvas.width = window.innerWidth;
	h = lightning_canvas.height = window.innerHeight;
	
	opts.maxRadius = Math.sqrt( w*w/4 + h*h/4 );
	opts.cx = w / 2;
	opts.cy = h / 2;
	
	init();
});
lightning_canvas.addEventListener( 'click', function(e){
	
	opts.cx = e.clientX;
	opts.cy = e.clientY;
	
})