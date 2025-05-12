//---------------------------------------------------------------------
sio.on('connect', () =>{
    console.log('Connected');
    sio.emit('sum', {numbers: [1,2]});
})

sio.on('disconnect', () => {
    console.log('Disconnected');
})

sio.on('showimage', (data) => {
    console.log(data);
    imageSound = document.getElementById('imageChat');
    imgChat = document.getElementById('imgChat');

    //imageSound.classList.remove('invisible');
    imgChat.src=data;
    imageSound.classList.add('show');

    setTimeout(() => {
        imageSound = document.getElementById('imageChat');
        imageSound.classList.remove('show');
    }, 5000);
})

sio.on('chatmsg', (data) => {
    console.log('chatmsg : ' + data);
    addChatMessage(data[0],data[1])
})

function myFunctionMessage() {

    var userName = document.getElementById("user").value;
    var messageTXT = document.getElementById("msg").value;

    addChatMessage(userName,messageTXT + Date.now().toString())
}

function addChatMessage(UserName, Message)
{
    var maxNumberOfMessages = 7;

    TwitchChat = document.getElementById('TwitchChat');

    TwitchChatMessageContainer = document.createElement('div');
    TwitchChatMessageContainer.classList.add('chat-Message-Container');

    TwitchChatUser = document.createElement('div');
    TwitchChatUser.classList.add('chat-User');
    TwitchChatUser.innerHTML = UserName;

    TwitchChatMessage = document.createElement('div');
    TwitchChatMessage.classList.add('chat-Message');
    TwitchChatMessage.innerHTML = Message;

    // Chat User Div Element    -------> TwitchChatMessageContainer
    // Chat Message Div Element -------> TwitchChatMessageContainer

    TwitchChatMessageContainer.append(TwitchChatUser);
    TwitchChatMessageContainer.append(TwitchChatMessage);

    TwitchChat.insertAdjacentElement('afterbegin', TwitchChatMessageContainer);

    console.log('length' + TwitchChat.children.length);

    if(TwitchChat.children.length >= maxNumberOfMessages)
    {
        TwitchChat.removeChild(TwitchChat.lastChild);
    }

    for (let msgId = 0; msgId < TwitchChat.children.length; msgId++)
    {
        TwitchChat.children[msgId].classList.add('chat-Scrolling')
        TwitchChat.children[msgId].addEventListener("animationend", () => {
            TwitchChat.children[msgId].classList.remove('chat-Scrolling');
        });
    }
}
