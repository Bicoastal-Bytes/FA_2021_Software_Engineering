fetch('/api/remaining')
    .then(function (response) {
        return response.json();
    })
    .then(function(data) {
        appendData(data);
    })
    .catch(function(err){
        console.log(`Error: ${err}`)
    })

var table = document.querySelector("#connected-players-table");
const roomName = JSON.parse(document.getElementById('game-room').textContent);
const userName = JSON.parse(document.getElementById('user-name').textContent);
let userList = null;
let activePlayer = null;
let category = null;
let question = null;
let choices = null;
let questionPoint = null;

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
    let chat_log = document.querySelector('#chat-log');
    switch(data.event) {
        case "JOIN":
            fetch('/api/table')
            .then((resp) => resp.json())
            .then(function(resp_data) {
                let table_data = JSON.parse(resp_data);
                userList = table_data;
                console.log(`Recieved Data Joining:${resp_data}`);
                chat_log.value += (data.message + '\n');
                console.log(table_data)
                deleteTableData(table);
                generateTable(table, table_data);
                let header = Object.keys(table_data[0]);
                generateTableHead(table, header);
            });

            fetch('/api/active')
            .then((response) => response.json())
            .then(function(incoming) {
                activePlayer = incoming.player;
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
           
            turnOn(category);
            break;
        case 'CHOOSE':

        // case "UPDATE_TABLE":
        //     generateTable(table, data.connected_users);
        //     generateTableHead(table, data.connected_users[0])
        //     break;
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

document.querySelector('#spin-button').onclick = function(e) { 
    fetch('api/category')
    .then((response) => response.json())
    .then(function(data) {
        category = data.category;
    });
    chatSocket.send(JSON.stringify({
        'event': 'SPIN',
        'element': 'buzzer',
        'category': category
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