let table = document.querySelector("#connected-players-table");
const roomName = JSON.parse(document.getElementById('game-room').textContent);
const userName = JSON.parse(document.getElementById('user-name').textContent);
const chat_log = document.querySelector('#chat-log');
let userList = null;
let activePlayer = null;
let category = null;
let question = null;
let choices = null;
let questionPoint = null;
let correctAnswer = null;
let questionsLeft = null;
let questionID = null;

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/game/'
    + roomName
    + '/'
);

chatSocket.onopen = function(e){
    chatSocket.send(JSON.stringify({
        'event': "JOIN",
        'message': `Welcome to Wheel of Jeopardy, ${userName}!`,
        'user_name': userName
    }));
}

/*
=============================================
Process events coming from the socket
=============================================
*/
chatSocket.onmessage = function(e) {
    let data = JSON.parse(e.data);
    data = data.payload;
    
    console.log(data.event);
    switch(data.event) {
        case "JOIN":
            getPlayerData(data);            
            fetch('/api/active')
            .then((response) => response.json())
            .then(function(incoming) {
                activePlayer = incoming.player;
            });

            fetch('/api/remaining')
            .then(resp => resp.json())
            .then(function(data) {
                questionsLeft = data.remaining_questions;
            });
            break;
        
        case 'SEND':
            chat_log.value += (data.message + '\n');
            break;
        
        case 'LEAVE':
            fetch('/api/table')
            .then((resp) => resp.json())
            .then(function(resp_data) {
                console.log(`Recieved Data leaving: ${resp_data}`)
            });
            deleteRow(data.user_name);
            chat_log.value += (data.message + '\n');
            break;
        
        case 'SPIN':
            category = data.category;
            calculatePrize(data.id);
            break;

        case 'CHOOSE':
            question = data.question;
            choices = data.choices;
            correctAnswer = data.correct_answer;
            questionID = data.question_id;
            turnOn('buzzer');
            break;
        
        case 'ANSWER':
            console.log('Got an answer')
            document.getElementById('result_result').innerHTML = data.message;
            if (activePlayer !== userName){
                turnOn('result');
            }
            fetch('/api/remaining')
            .then(function (response) {
                return response.json();
            })
            .then(function(data) {
                questionsLeft = data.remaining_questions;
                getPlayerData(data);
            })
            .catch(function(err){
                console.log(`Error: ${err}`);
            });
            break;
            
        case 'BUZZ':
            activePlayer = data.player;
            turnOn('answer');
            break;
        
        case 'START':
            turnOn('wheel');
            break;
    }
};

chatSocket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};

/*
=============================================
Functions to handle user events
=============================================
*/
document.querySelector('#chat-message-input').onkeyup = function(e) {
    if (e.keyCode === 13) {  // enter, return
        document.querySelector('#chat-message-submit').click();
    }
};


document.querySelector('#spinthewheel').onclick = function(e) { 
    let id = 0;
    fetch('/api/category')
    .then((response) => response.json())
    .then(function(data) {
        category = data.category;
        id = data.id;
        chatSocket.send(JSON.stringify({
            'event': 'SPIN',
            'category': category,
            'id': id
        }));
    });
   
}

document.querySelector('#start-game-button').onclick = function(e) {
    chatSocket.send(JSON.stringify({
        'event': 'START'
    }));
}

document.querySelector('#next-button').onclick = function(e) {
    chatSocket.send(JSON.stringify({
        'event': 'START'
    }));
}

document.querySelector('#chat-message-submit').onclick = function(e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'event': 'SEND',
        'message': message
    }));
    messageInputDom.value = '';
};

// Leave game 
document.querySelector("#leave-game-button").onclick = function(e) {
    chatSocket.send(JSON.stringify({
        'event': 'LEAVE',
        'message': `${userName} has left the room`,
        'user_name': userName
    }));
    const user = {player: userName}
    fetch('/api/unregister', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(user)
    })
    .then(response => response)
    .then(data => {
        window.location.href = '/';
    })
    .catch((error) => {
        console.error('Error', error);
    });
}; 