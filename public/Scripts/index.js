//---------------------------------------------------------------------
sio.on('connect', () =>{
    console.log('Connected');
    sio.emit('sum', {numbers: [1,2]});
})

sio.on('disconnect', () => {
    console.log('Disconnected');
})

sio.on('sumResult', (data) => {
    console.log(data);
})

sio.on('msg', (data) => {
    console.log(data);
    data = data.replace(/(<([^>]+)>)/ig,"");
    console.log(data);
    //Scroller = document.getElementById('Scroller');
    //Scroller.innerHTML = data;
    ScrollMessage(data)
})

sio.on('plasma', (data) => {
    console.log(data);
    plasmaCanvas = document.getElementById('canvas');
    lightning_canvas = document.getElementById('lightning_canvas');
    Sprial = document.getElementById('Sprial');
    protonFig_canvas = document.getElementById('protonFig_canvas');

    argument = data.toLowerCase()
    switch (argument) {
        case 'plasma':
            plasmaCanvas.classList.remove('invisible');
            lightning_canvas.classList.add('invisible');
            Sprial.classList.add('invisible');
            protonFig_canvas.classList.add('invisible');
            break;
        case 'lightning':
            plasmaCanvas.classList.add('invisible');
            lightning_canvas.classList.remove('invisible');
            Sprial.classList.add('invisible');
            protonFig_canvas.classList.add('invisible');
            break;
        case 'spiral':
            plasmaCanvas.classList.add('invisible');
            lightning_canvas.classList.add('invisible');
            Sprial.classList.remove('invisible');
            protonFig_canvas.classList.add('invisible');
            break;
        case 'ocean':
            plasmaCanvas.classList.add('invisible');
            lightning_canvas.classList.add('invisible');
            Sprial.classList.add('invisible');
            protonFig_canvas.classList.remove('invisible');
            break;
        default:
            plasmaCanvas.classList.add('invisible');
            lightning_canvas.classList.add('invisible');
            Sprial.classList.add('invisible');
            protonFig_canvas.classList.add('invisible');
            break;
    }
})

sio.on('backcolour', (data) => {
    console.log(data);
    app = document.getElementById('app');
    app.style.backgroundColor = data;
    lightness = 1 - getLightnessOfRGB(hexToRgb(data)).toFixed(4);;

    latestSub = document.getElementById('LatestSub');
    LatestFollow = document.getElementById('LatestFollow');
    LatestCheer = document.getElementById('LatestCheer');
    socDiscord = document.getElementById('socDiscord');
    socTwitter = document.getElementById('socTwitter');
    socWeb = document.getElementById('socWeb');
    ChannelOwner = document.getElementById('ChannelOwner');
    StreamTitle = document.getElementById('StreamTitle');
    if (lightness > 0.6) 
    {
        latestSub.style.color = 'white';
        LatestFollow.style.color = 'white';
        LatestCheer.style.color = 'white';
        socDiscord.style.color = 'white';
        socTwitter.style.color = 'white';
        socWeb.style.color = 'white';
        ChannelOwner.style.color = 'white';
        StreamTitle.style.color = 'white';
    }
    else
    {
        //latestSub.style.color = 'rgb(' + 255 * lightness + ',' + 255 * lightness + ',' + 255 * lightness + ')';
        latestSub.style.color = 'black';
        LatestFollow.style.color = 'black';
        LatestCheer.style.color = 'black';
        socDiscord.style.color = 'black';
        socTwitter.style.color = 'black';
        socWeb.style.color = 'black';
        ChannelOwner.style.color = 'black';
        StreamTitle.style.color = 'black';
    }
    console.log(lightness);
})

function hexToRgb(h) {
    var r = parseInt(cutHex(h).substring(0, 2), 16),
        g = parseInt(cutHex(h).substring(2, 4), 16),
        b = parseInt(cutHex(h).substring(4, 6), 16);
    return "rgb(" + r + "," + g + "," + b + ")";
}

function cutHex(h) {
    return h.charAt(0) == "#" ? h.substring(1, 7) : h;
}

function getLightnessOfRGB(rgbString) {
    // First convert to an array of integers by removing the whitespace, taking the 3rd char to the 2nd last then splitting by ','
    const rgbIntArray = (rgbString.replace(/ /g, '').slice(4, -1).split(',').map(e => parseInt(e)));

    // Get the highest and lowest out of red green and blue
    const highest = Math.max(...rgbIntArray);
    const lowest = Math.min(...rgbIntArray);

    //const average = Math.average(...rgbIntArray);
    const average = rgbIntArray.reduce((a, b) => a + b, 0) / rgbIntArray.length;

    // Return the average divided by 255
    //return (highest + lowest) / 2 / 255;
    return average / 255;
}

sio.on('title', (data) => {
    console.log(data);
    StreamTitle = document.getElementById('StreamTitle');
    StreamTitle.innerHTML = data;
})

sio.on('init', (data) => {
    console.log(data);
    LatestSub = document.getElementById('LatestSub');
    LatestFollow = document.getElementById('LatestFollow');
    LatestCheer = document.getElementById('LatestCheer');

    LatestSub.innerHTML = 'Last Subscriber:<br>' + data[0] + ' (' + data[1] + ')';
    LatestFollow.innerHTML = 'Last Follower:<br>' + data[2]
    LatestCheer.innerHTML = 'Last Cheer:<br>' + data[3] + ' (' + data[4] + ')';
})

sio.on('sub', (data) => {
    console.log(data);
    LatestSub = document.getElementById('LatestSub');
    LatestSub.innerHTML = innerHTML = 'Last Subscriber:<br>' + data[0] + ' (' + data[1] + ' Months)';
})

sio.on('follow', (data) => {
    console.log(data);
    LatestFollow = document.getElementById('LatestFollow');
    LatestFollow.innerHTML = innerHTML = 'Last Follower:<br>' + data[0];
})

sio.on('cheer', (data) => {
    console.log(data);
    LatestCheer = document.getElementById('LatestCheer');
    LatestCheer.innerHTML = innerHTML = 'Last Cheer:<br>' + data[0] + ' (' + data[1] + ' Bits)';
})

sio.on('listen', (data) => {
    console.log(data);
    audioChat = document.getElementById('audioChat');
    imageSound = document.getElementById('hideMeAfter5Seconds');
    audioChat.src = data;
    audioChat.play();
})

this.messageQueue = [];
this.messageInProgress = false;

//------------------------------------------------------------------------
function ScrollMessage(message)
{
    this.messageQueue.push(message);

    if (this.messageInProgress == false)
    {
        this.messageScrolling();
    }
}

//---------------------------------------------------------------------
async function messageScrolling(divControl)
{
    const BotScroller = document.getElementById('ScrollerAds');
    const divBanner = document.getElementById('Banner');

    while ((this.messageQueue.length > 0 && this.messageInProgress == false))
    {
        divControl = document.createElement('marquee');
        divControl.classList.add('ScrollerMsg');
        divBanner.append(divControl);

        BotScroller.stop();
        BotScroller.classList.add('invisible');
        divControl.classList.remove('invisible');

        console.log(divControl);

        console.log('Grad Message From Queue');
        var message = this.messageQueue.shift();

        console.log('Send Message To Overlay');
        divControl.innerHTML = message;
        divControl.start();

        timeForDelay = 16000 + (350*message.length)
        this.messageInProgress = true;
        console.log('Start Delay');
        await sleep(timeForDelay);
        console.log('EndDelay Delay');
        divControl.stop();

        this.messageInProgress = false;

        console.log(messageQueue.length)
        BotScroller.classList.remove('invisible');
        divControl.classList.add('invisible');

        divBanner.removeChild(divControl);
        BotScroller.start();
    }
    
    function sleep(ms)
    {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
