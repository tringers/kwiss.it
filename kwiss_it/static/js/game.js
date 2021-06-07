const lobbyDiv = document.getElementById('lobby')
const gameDiv = document.getElementById('game')
const qHeader = document.getElementById('qHeader');
const qhCategory = document.getElementById('qhCategory');
const qhCurrentQuestion = document.getElementById('qhCurrentQuestion');
const qhMaxQuestion = document.getElementById('qhMaxQuestion');
const qhQuestion = document.getElementById('qhQuestion');
const qhType = document.getElementById('qhType');
const timeBar = document.getElementById('timeBar');
const submitAnswer = document.getElementById('submitAnswer');
const answerRow = document.getElementById('answers');
const qResult = document.getElementById('qResult');
let doneMessage = false;
let isDeviation = false;

function prepGame() {
    qhMaxQuestion.innerHTML = game.meta.maxQuestions;

    if (game.meta.timeStarted === 0) {
        // Prepare game (5s delay)
        stopHeartbeat();
        heartbeat = setInterval(sendHeartbeat, 500);
        for (let i = 0; i < 6; i++) {
            setTimeout(() => {
                let lobbyDelayTime = document.getElementById('lobbyDelayTime');
                lobbyDelayTime.innerHTML = "Start in " + (5 - i) + "s";
                if (i === 5) {
                    startGame();
                }
            }, 1000 * (i + 1));
        }
    }
}

function getTimestamp_ms() {
    return new Date().valueOf();
}

function getTimestamp_s() {
    return Math.floor(getTimestamp_ms() / 1000);
}

function startGame() {
    lobbyDiv.classList.add('invisible');
    lobbyDiv.hidden = true;
    gameDiv.classList.remove('invisible');
    gameDiv.hidden = false;
    game.meta.timeStarted = getTimestamp_s();
    game.interval = setInterval(connectionHandle, 50);
}

function connectionHandle() {
    let questionNo = whichQuestion();

    if (questionNo === game.processedQuestion && !is_question()) {
        if (!game.lastSubmitted) {
            game.lastSubmitted = true;
            submitAnswer.disabled = true;
            answerSubmission([-1]);
        }
        // Disable Answer section and wait for server to send resolution
        if (!game.scoresFetched) {
            game.scoresFetched = true;
            setTimeout(getStatus, 5000);
        }
    }

    if (questionNo !== game.processedQuestion && questionNo < game.meta.maxQuestions) {
        hideQuestionResult();
        game.processedQuestion = questionNo;
        loadQuestion();
        game.gamedata[first_name].lastSubmissionCorrect = false;
        game.lastSubmitted = false;
        submitAnswer.disabled = false;
        game.scoresFetched = false;
        resetVotebutton();
    }

    if((questionNo + 1) === game.meta.maxQuestions && !is_question()) {
        clearInterval(game.interval);
        clearInterval(heartbeat);
        if(!doneMessage) {
            doneMessage = true;
            let backButton = document.getElementById('backLobby');
            backButton.hidden = false;
            backButton.addEventListener('click', () => {
                window.location.href = base_url + '/lobbylist';
            });
        }
    } else {
        timeBar.style.width = Math.round(100 - timeElapsed() * 100 / game.meta.timePerQuestion) + '%';
    }
}

async function sendHeartbeat() {
    await fetch('/lobby/heartbeat/' + lobby_key);
}

async function loadQuestion() {
    // Fetch everything
    let questionNo = whichQuestion();

    let question = document.getElementById('question-' + questionNo);
    let cName = question.getAttribute('data-cname');
    let cId = question.getAttribute('data-cid');
    let qText = question.getAttribute('data-qtext');
    let qId = question.getAttribute('data-qid');
    qText = await decrypt(qText, lobby_key);
    let qType = question.getAttribute('data-qtype');

    let answersAll = document.getElementsByClassName('answer-question-' + questionNo);
    let answers = [];

    for (let i = 0; i < answersAll.length; i++) {
        let anum = answersAll[i].getAttribute('data-anum');
        let atext = answersAll[i].getAttribute('data-atext');

        answers.push({
            anum: parseInt(anum),
            atext: await decrypt(atext, lobby_key),
        })
    }

    // Set everything
    let qtid = parseInt(qType);
    let qtype_obj = game.meta.qTypes.getQuestionType(qtid);

    qhCategory.innerHTML = cName;
    qhCategory.setAttribute('data-cid', cId);
    qhCurrentQuestion.innerHTML = (questionNo + 1).toString();
    qhQuestion.innerHTML = qText;
    qhQuestion.setAttribute('data-qid', qId);
    qhType.innerHTML = qtype_obj.description;
    timeBar.style.width = Math.round(100 - timeElapsed() * 100 / game.meta.timePerQuestion) + '%';

    loadAnswers(qtid, answers);
}

function loadAnswers(qtid, answers) {
    switch (qtid) {
        // case 1 and 4 -> ignore answers
        case 1:
            answerRow.innerHTML = '';

            let qt1_copy = document.getElementById('qtype_temp1').cloneNode(true);

            qt1_copy.id = 'qtype_1_1';
            qt1_copy.classList.remove('template');
            qt1_copy.innerHTML = qt1_copy.innerHTML.replaceAll('temp1', '1_1');

            answerRow.appendChild(qt1_copy);
            break;
        case 2:
            answerRow.innerHTML = '';

            for (let i = 0; i < answers.length; i++) {
                let anum = answers[i].anum;
                let atext = answers[i].atext;

                let qt2_copy = document.getElementById('qtype_temp2').cloneNode(true);

                qt2_copy.id = 'qtype_2_' + i;
                qt2_copy.classList.remove('template');
                qt2_copy.innerHTML = qt2_copy.innerHTML.replaceAll('temp2', '2_' + i);

                answerRow.appendChild(qt2_copy);

                let inputField = document.getElementById('answer_2_' + i);
                let inputLabel = document.getElementById('answerLabel_2_' + i);
                inputField.value = anum;
                inputLabel.innerHTML = atext;
            }
            break;
        case 3:
            answerRow.innerHTML = '';

            for (let i = 0; i < answers.length; i++) {
                let anum = answers[i].anum;
                let atext = answers[i].atext;

                let qt3_copy = document.getElementById('qtype_temp3').cloneNode(true);

                qt3_copy.id = 'qtype_3_' + i;
                qt3_copy.classList.remove('template');
                qt3_copy.innerHTML = qt3_copy.innerHTML.replaceAll('temp3', '3_' + i);

                answerRow.appendChild(qt3_copy);

                let inputField = document.getElementById('answer_3_' + i);
                let inputLabel = document.getElementById('answerLabel_3_' + i);
                inputField.value = anum;
                inputLabel.innerHTML = atext;
            }
            break;
        case 4:
            answerRow.innerHTML = '';

            let qt4_copy = document.getElementById('qtype_temp4').cloneNode(true);

            qt4_copy.id = 'qtype_4_1';
            qt4_copy.classList.remove('template');
            qt4_copy.innerHTML = qt4_copy.innerHTML.replaceAll('temp4', '4_1');

            answerRow.appendChild(qt4_copy);
            break;
    }
}

async function postData(url = '', data = {}) {
    const response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        credentials: 'same-origin',
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(data),
    });
    return response.json();
}

function whichQuestion() {
    let delta = Math.abs(game.meta.timeStarted - getTimestamp_s());
    let questionPause = game.meta.timePerQuestion + 15;
    return Math.floor(delta / questionPause);
}

function is_question() {
    let delta = Math.abs(game.meta.timeStarted - getTimestamp_s());
    let questionLength = game.meta.timePerQuestion;
    let questionPause = game.meta.timePerQuestion + 15;
    let currentQuestionTime = delta % questionPause;
    return currentQuestionTime < questionLength;
}

function timeElapsed() {
    // Between starttime of question and current timestamp
    return Math.abs(game.meta.timeStarted + (whichQuestion() * (game.meta.timePerQuestion + 15)) - getTimestamp_s());
}

function answerSubmission(answer = [-1]) {
    if(answer.length === 0)
        answer.push(-1);

    postData(base_url + '/game/' + lobby_key, {
        lobbyAuth: lobby_auth,
        name: first_name,
        qno: whichQuestion() + 1,
        answer: answer,
    })
        .then(json => {
            if(json.checkLater)
                return;
            let myResult = document.getElementById('myResult');
            myResult.classList.remove('text-success');
            myResult.classList.remove('text-danger');

            if (json.lastSubmissionCorrect) {
                myResult.classList.add('text-success');
                myResult.innerHTML = "Korrekte Antwort!";
            } else {
                myResult.classList.add('text-danger');
                myResult.innerHTML = "Falsche Antwort!";
            }

            let myAddition = document.getElementById('myAddition');
            let myStreak = document.getElementById('myStreak');
            let myScore = document.getElementById('myScore');
            myAddition.innerHTML = json.addition;
            myStreak.innerHTML = json.streak;
            myScore.innerHTML = json.score;
        });
}

function showQuestionResult() {
    // Update others results
    let gamedata_keys = Object.keys(game.gamedata);
    let overallResult = document.getElementById('overallResult');
    overallResult.innerHTML = '';

    for (let i = 0; i < gamedata_keys.length; i++) {
        let gamedata = game.gamedata[gamedata_keys[i]];

        if (gamedata_keys[i] === first_name && !isDeviation)
            continue;
        else if(gamedata_keys[i] === first_name && isDeviation) {
            let myResult = document.getElementById('myResult');
            myResult.classList.remove('text-success');
            myResult.classList.remove('text-danger');

            if (gamedata.lastSubmissionCorrect) {
                myResult.classList.add('text-success');
                myResult.innerHTML = "Korrekte Antwort!";
            } else {
                myResult.classList.add('text-danger');
                myResult.innerHTML = "Falsche Antwort!";
            }

            let myAddition = document.getElementById('myAddition');
            let myStreak = document.getElementById('myStreak');
            let myScore = document.getElementById('myScore');
            myAddition.innerHTML = gamedata.addition;
            myStreak.innerHTML = gamedata.streak;
            myScore.innerHTML = gamedata.score;
            continue;
        }

        let otherRow = document.createElement('tr');
        let otherName = document.createElement('td');
        let otherAddition = document.createElement('td');
        let otherStreak = document.createElement('td');
        let otherScore = document.createElement('td');

        if (gamedata.lastSubmissionCorrect) {
            otherRow.classList.add('table-success');
        } else {
            otherRow.classList.add('table-danger');
        }

        otherAddition.classList.add('text-center');
        otherStreak.classList.add('text-center');
        otherScore.classList.add('text-center');

        otherName.innerHTML = gamedata_keys[i];
        otherAddition.innerHTML = gamedata.addition;
        otherStreak.innerHTML = gamedata.streak;
        otherScore.innerHTML = gamedata.score;

        otherRow.appendChild(otherName);
        otherRow.appendChild(otherAddition);
        otherRow.appendChild(otherStreak);
        otherRow.appendChild(otherScore);
        overallResult.appendChild(otherRow);
    }

    answerRow.classList.add('invisible');
    qResult.classList.remove('invisible');
}

function hideQuestionResult() {
    answerRow.classList.remove('invisible');
    qResult.classList.add('invisible');
}

function getStatus() {
    fetch(base_url + '/game/' + lobby_key)
        .then(data => data.json()
            .then(json => {
                isDeviation = json.deviation;

                for (let i = 0; i < json.results.length; i++) {
                    let playerData = json.results[i];
                    let data = Object.assign(playerScoreTemplate, game.gamedata[playerData.name]);
                    data.streak = playerData.streak;
                    data.score = playerData.score;
                    data.addition = playerData.addition;
                    game.gamedata[playerData.name] = data;
                }

                showQuestionResult();
            }));
}

function getEndscreen() {
    // TODO: Show placement of all player
    // TODO: Show created reports
    alert("DONE");
}

submitAnswer.addEventListener('click', () => {
    submitAnswer.disabled = true;
    if (!game.lastSubmitted) {
        game.lastSubmitted = true;
        let answers = [];
        let checkSelection = document.getElementsByName('answer');

        for (let i = 0; i < checkSelection.length; i++) {
            if(checkSelection[i].id.indexOf('answer_temp') >= 0)
                continue;

            if (checkSelection[i].checked || checkSelection.length === 5) {
                answers.push(checkSelection[i].value);
            }
        }
        answerSubmission(answers);
    }
})