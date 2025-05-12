//---------------------------------------------------------------------
sio.on('connect', () =>{
    console.log('Connected');
    sio.emit('sum', {numbers: [1,2]});
})

sio.on('disconnect', () => {
    console.log('Disconnected');
})

sio.on('gamestart', (data) => {
    console.log(data);
    gameStatus = document.getElementById('gameStatus');
    gameTitle = document.getElementById('gameTitle');
    gameStatus.style.left = 1152
    clearOutPreviousDisplay()
    gameTitle.innerHTML = data;
})

sio.on('gameupdate', (data) => {
    console.log(data);
    gameStatus = document.getElementById('gameStatus');
    createPlayerDisplay(data);
})

sio.on('gameended', (data) => {
    console.log(data);
    gameStatus = document.getElementById('gameStatus');
    gameStatus.style.left = 1452
})

function clearOutPreviousDisplay()
{
    gameStatus = document.getElementById('gameStatus');

    gamePlayers = document.getElementById('gamePlayers');
    gamePlayers.remove()
    gamePlayers = null;

    const newGamePlayers = document.createElement('div');
    newGamePlayers.setAttribute('id', 'gamePlayers');
    gameStatus.appendChild(newGamePlayers);
}

function createPlayerDisplay(data)
{
    clearOutPreviousDisplay()

    gameStatus = document.getElementById('gameStatus');
    gamePlayers = document.getElementById('gamePlayers');
    gameTitle = document.getElementById('gameTitle').innerHTML;

    voteTotal = 0;
    voteCount = 0;
    data.forEach((dataitem, dataitemindex) => {
        console.log(dataitem);
        const gamePlayer = document.createElement('div');
        gamePlayer.setAttribute('id','player-'+dataitemindex);
        gamePlayer.classList.add('gamePlayer');

        if (gameTitle == 'vote'){
            gamePlayer.style.top = dataitemindex * 17
            gamePlayer.innerHTML = dataitem[0] + ' : ' + dataitem[1];
            voteTotal += parseInt(dataitem[1]);
            voteCount = dataitemindex + 1;
        }
        else{
            gamePlayer.style.top = dataitemindex * 35
            gamePlayer.innerHTML = dataitem[0];
    
            const gameGuess = document.createElement('div');
            gameGuess.classList.add('gameGuess');
            gameGuess.innerHTML = '#' + dataitem[1].attemptNo + ' : ' + dataitem[1].attempt;
    
            const gameResult = document.createElement('div');
            gameResult.classList.add('gameResult');
    
            dataitem[1].result.forEach((dataItemResult, dataItemResultIndex) => {
                const gameResultItem = document.createElement('div');
                gameResultItem.classList.add('gameResultDefault');
    
                if (dataItemResult == 'B' || dataItemResult == 'W'){
                    gameResultItem.classList.add('gameResultDefault' + dataItemResult)
                }
                gameResultItem.style.left = (dataItemResultIndex * 22) + 2
    
                gameResult.appendChild(gameResultItem)
            })
    
            gamePlayer.appendChild(gameGuess);
            gamePlayer.appendChild(gameResult);
        }
        gamePlayers.appendChild(gamePlayer);
    });

    if (gameTitle == 'vote'){
        const gamePlayer = document.createElement('div');
        gamePlayer.setAttribute('id','player-Avg');
        gamePlayer.classList.add('gamePlayer');    
        gamePlayer.innerHTML = "Current Average Is " + parseInt(voteTotal / voteCount)
        gamePlayers.appendChild(gamePlayer);

        gamePlayer.style.top = (voteCount+1) * 17
    }
    //console.log(voteTotal, voteCount);
}
//----------------------------------------------------------------------------------------------------------
sio.on('pollstart', (data) => {
    console.log(data);

    pollRegion = document.getElementById('pollRegion');
    pollQuestion = document.getElementById('pollQuestion');
    pollYes = document.getElementById('pollYes');
    pollNo = document.getElementById('pollNo');
    pollRegion.style.top = 700;
    pollQuestion.innerHTML = data[0];    
    pollYes.innerHTML = data[1];    
    pollNo.innerHTML = data[2];    
})

//----------------------------------------------------------------------------------------------------------
sio.on('pollupdate', (data) => {
    console.log(data);
    pollBarLeft = document.getElementById('pollBarLeft');
    pollBarRight = document.getElementById('pollBarRight');

    pollBarLeft.innerHTML = (data[0] > 10) ? data[0] + '%' :"";
    pollBarRight.innerHTML = (data[1] > 10) ? data[1] + '%' :"";

    pollBarLeft.style.width= data[0] + '%'
    pollBarRight.style.width= data[1] + '%'
})

//----------------------------------------------------------------------------------------------------------
sio.on('pollended', (data) => {
    console.log(data);

    pollRegion = document.getElementById('pollRegion');
    pollRegion.style.top = 900;
})

