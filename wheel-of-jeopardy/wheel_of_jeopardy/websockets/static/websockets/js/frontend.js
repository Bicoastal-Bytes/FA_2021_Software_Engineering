
var buzzerStart = 0; 
var elapsedTime = 0;   
var splits = null;      // this variable splits up the question answer
var splitschoice = 0;   


/* ************************ */
/* this is for debugging    */
/* ************************ */

function turnOn (whichDiv, choice = null) {
    var original;
    var result;
    var myList;

    document.getElementById('debugging').innerHTML = 'userList: ' + userList + '<br>' + 'activePlayer: ' + activePlayer + '<br>' + 'category: ' + category  + '<br>' + 'question: ' + question  + '<br>' + 'choices: ' + choices + '<br>' + 'questionPoint: ' + questionPoint  + '<br>' + 'correctAnswer: ' + atob(correctAnswer) + '<br>';

    turnOff(); 
    document.getElementById(whichDiv).style.display = 'block';

    if (choice != null) {
        const answer_data = {
            'question_id': questionID,
            'answer': splits[choice]
        }
        fetch('/api/validate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(answer_data)
        })
        .then(resp => resp.json())
        .then(function(data){
            var correctMessage = (data.answer == true) ? 'correctly' :'incorrectly';
            var whoMessage = (activePlayer = userName) ? 'You' : activePlayer;
            let message = `${whoMessage}' answered the question ${correctMessage}.`;
            chatSocket.send(JSON.stringify({
                'event': 'ANSWER',
                'message': message,
                'userChoice': splits[choice]
            }));
        })
    }                
    
    if (whichDiv == 'wheel') {
        /* reset turned off divs for next turn */
        myList = ["button10", "button20", "button30", "button40", "button50"];
        disableEnable(myList, 'enable');
        myList = ["buttona", "buttonb", "buttonc", "buttond"]
        disableEnable(myList, 'enable');
        /* hide spin the wheel button if inactive player */
        if (userName != activePlayer){
            document.getElementById('spinthewheel').style.display = 'none';
        }
    } else if (whichDiv == 'buzzer') {
        /* parse the answers */                    
        var mystring = JSON.stringify(choices);                    
        var newmystring = mystring.replace('[', '').replace(']', '').replace(/"/g, '');
        splits = newmystring.split(",");

        /* populates the question on both buzzer, answer pages and result page */
        document.getElementById('buzzercategory').innerHTML = category;     document.getElementById('answercategory').innerHTML = category;
        document.getElementById('buzzerquestion').innerHTML = question;     document.getElementById('answerquestion').innerHTML = question;
        document.getElementById('buzzeranswers').innerHTML = 'A. ' + splits[0] + ' B. ' + splits[1] + ' C. ' + splits[2] + ' D. ' + splits[3];       
        document.getElementById('answeranswers').innerHTML = 'A. ' + splits[0] + ' B. ' + splits[1] + ' C. ' + splits[2] + ' D. ' + splits[3];  
        document.getElementById('resultcorrectanswer').innerHTML = 'The correct answer was - ' + atob(correctAnswer);
        /* puts 5 second countdown timer on buzzer screen */
        display = document.querySelector('#time');
        startTimer(5, display);
        startBuzzer();
    } 
    
    if (userName == activePlayer) {
        document.getElementById(whichDiv + '_activediv').style.display = 'block';
        document.getElementById(whichDiv + '_inactivediv').style.display = 'none';
    } else {
        /* this deals with putting the active players name on the screen */
        if (whichDiv == 'wheel' || whichDiv == 'pointvalue' || whichDiv == 'answer' || whichDiv == 'result') {
            original = document.getElementById(whichDiv + '_inactivediv').innerHTML;
            result = original.substr(original.indexOf(" ") + 1);
            document.getElementById(whichDiv + '_inactivediv').innerHTML = activePlayer + ' ' + result;
        }

        /* grays out values for inactive player */
        if (whichDiv == 'pointvalue') {
            myList = ["button10", "button20", "button30", "button40", "button50"];
            disableEnable(myList, 'disable');
        }

        /* grays out question choices for inactive player */
        if (whichDiv == 'pointvalue') {
            myList = ["buttona", "buttonb", "buttonc", "buttond"]
            disableEnable(myList, 'disable');
        }
        document.getElementById(whichDiv + '_inactivediv').style.display = 'block';
        document.getElementById(whichDiv + '_activediv').style.display = 'none';
    }
}

/* this function turns buttons on and off */
function disableEnable (theList, status) {
    var arrayLength = theList.length;
    for (var i = 0; i < arrayLength; i++) {
        if (status == 'disable') {
            document.getElementById(theList[i]).disabled = true;    document.getElementById(theList[i]).style.backgroundColor = 'gray';    document.getElementById(theList[i]).style.cursor = 'not-allowed';
        } else {
            document.getElementById(theList[i]).disabled = false;    document.getElementById(theList[i]).style.backgroundColor = 'yellow';    document.getElementById(theList[i]).style.cursor = 'pointer';
        }
    }
}

function startBuzzer () {
    let buzzerStart = Date.now();
    elapsedTime = 0             // reset buzzer & elapsedTime = 0 means no buzzer press

    setTimeout(() => {
        turnOn('answer');
    }, 7000);                 
}

function stopBuzzer () {
        elapsedTime = Math.floor((Date.now() - buzzerStart));
        console.log('buzzer milliseconds: ' + elapsedTime);
        const user = {'player': userName}
        fetch('/api/buzz', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(user)
        })
        .then(resp => resp.json())
        .then(function(data) {
            chatSocket.send(JSON.stringify({
                'event': 'BUZZ',
                'player': data.active_player,
                'time': elapsedTime
            }));
        })
        /* turnOn('answer'); */ /* i have a bug here where if you press this it still forwards in 5 seconds */
}

function sendPoints (pointValue) {
    fetch(`/api/question?category=${category}&points=${pointValue}`)
    .then((resp) => resp.json())
    .then(function(data) {
        let t_question = data.question;
        questionID = data.question_id;
        let t_choices = data.choices;
        choicesID = data.choices_id;
        let t_correctAnswer = data.correct_answer;
    chatSocket.send(JSON.stringify({
        'event': "CHOOSE",
        'question': t_question,
        'choices': t_choices,
        'correct_answer': t_correctAnswer
        }));
    });
}

/* countdown timer for the buzzer screen */

function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);
    
        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;
    
        display.textContent = seconds;
    
        if (--timer < 0) {
            timer = duration;
        }
    }, 1000);
    }

    
function turnOff () {
    const pageNames = [ {x:'status'}, {x:'wheel'}, {x:'pointvalue'}, {x:'buzzer'}, {x:'answer'}, {x:'result'}, {x:'gameresult'}];
    pageNames.forEach((element) => {
        document.getElementById(element.x).style.display = 'none';
    });
}