// static/websockets/js/helpers.js

async function postData(url = '', data = {}) {
    const response = await fetch(url , {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return response.json();
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function getCategory() {
   let response =  fetch('/')
}

function getPlayerData(data){
    fetch('/api/table')
    .then((resp) => resp.json())
    .then(function(resp_data) {
        let table_data = JSON.parse(resp_data);
        userList = table_data;
        console.log(`Recieved Data Joining:${table_data}`);
        chat_log.value += (data.message + '\n');
        console.log(table_data)
        deleteTableData(table);
        generateTable(table, table_data);
        let header = Object.keys(table_data[0]);
        generateTableHead(table, header);
    });
}


function appendData(data) {
    var mainContainer = document.getElementById("id-remaining-questions");
    var div = document.createElement("div");
    console.log(data);
    div.innerHTML = `Remaining Questions: ${data.remaining_questions}`;
    mainContainer.appendChild(div);
}