class QTypes {
    qtid = [];
    qtname = [];
    qtdescription = [];

    addQuestionType(qtid, qtname, qtdescription) {
        this.qtid.push(qtid);
        this.qtname.push(qtname);
        this.qtdescription.push(qtdescription);
    }

    getQuestionType(qtid) {
        for (let i = 0; i < this.qtid.length; i++) {
            if (this.qtid[i] === qtid)
                return {name: this.qtname[i], description: this.qtdescription[i]};
        }
    }
}

const lobby_key = document.getElementById('lobby-data').getAttribute('data-lobby-key');
const lobby_auth = document.getElementById('lobby-data').getAttribute('data-auth-token');
const crypto_meta = document.getElementById('crypto');
const question_data = document.getElementById('question-data');
const answer_data = document.getElementById('answer-data');
const textenc = new TextEncoder();
const textdec = new TextDecoder();
const button_ready = document.getElementById('btnReady');
const playeramount = document.getElementById('playeramount');
let first_name = '';
let heartbeat_error = 0;
let game = {
    meta: {
        maxQuestions: 0,
        timeStarted: 0,
        timePerQuestion: 20,
        qTypes: new QTypes(),
    },
    interval: null,
    processedQuestion: -1,
    lastSubmitted: false,
    scoresFetched: false,
    gamedata: {
        lastSubmissionCorrect: false,
        streak: 1,
        score: 0,
        addition: 0,
    }
};
const playerScoreTemplate = {
    lastSubmissionCorrect: false,
    streak: 1,
    score: 0,
    addition: 0,
}

button_ready.addEventListener('click', () => {
    switch (parseInt(button_ready.getAttribute('data-value'))) {
        case 0:
            // Switch to "Ready"
            button_ready.value = "Nicht bereit";
            button_ready.setAttribute('data-value', "1");
            sendReadyStatus(true);
            break;
        case 1:
            // Switch to "Not Ready"
            button_ready.value = "Bereit";
            button_ready.setAttribute('data-value', "0");
            sendReadyStatus(false);
            break;
    }
})

function sendReadyStatus(ready) {
    fetch('/lobby/ready/' + lobby_key + '/' + ready.toString());
}


if (parseInt(crypto_meta.getAttribute('data-iv')) === 0) {
    // Generate IV for crypto
    let iv = crypto.getRandomValues(new Uint8Array(16));
    let data = iv.join(',');
    crypto_meta.setAttribute('data-iv', data);
}

function getIV() {
    let data = crypto_meta.getAttribute('data-iv');
    let array_str = data.split(',');
    let buffer = new ArrayBuffer(16);
    let view = new Uint8Array(buffer);
    for (let i = 0; i < array_str.length; i++)
        view[i] = parseInt(array_str[i]);

    return buffer;
}

async function encrypt(text, passwd) {
    const data = textenc.encode(text);

    const pw = textenc.encode(passwd);
    const pwHash = await crypto.subtle.digest('SHA-256', pw);

    const alg = {name: 'AES-GCM', iv: getIV()};
    const key = await crypto.subtle.importKey('raw', pwHash, alg, false, ['encrypt']);
    const encBuffer = await crypto.subtle.encrypt(alg, key, data);
    return abtob64(encBuffer);
}

async function decrypt(b64, password) {
    const pw = textenc.encode(password);
    const pwHash = await crypto.subtle.digest('SHA-256', pw);

    const alg = {name: 'AES-GCM', iv: getIV()};
    const key = await crypto.subtle.importKey('raw', pwHash, alg, false, ['decrypt']);

    const ctBuffer = b64toab(b64);
    const ptBuffer = await crypto.subtle.decrypt(alg, key, ctBuffer);

    return textdec.decode(ptBuffer);
}

function abtob64(buffer) {
    let binary = '';
    let bytes = new Uint8Array(buffer);
    let len = bytes.byteLength;
    for (let i = 0; i < len; i++) {
        binary += String.fromCharCode(bytes[i]);
    }
    return window.btoa(binary);
}

function b64toab(base64) {
    let binary_string = window.atob(base64);
    let len = binary_string.length;
    let bytes = new Uint8Array(len);
    for (let i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}

let heartbeat = setInterval(() => {
    fetch('/lobby/heartbeat/' + lobby_key)
        .then((data) => {
            data.json().then(json => {
                if (parseInt(json.status) === 200) {
                    if (first_name === '') {
                        first_name = json.name;
                        game.gamedata = {};
                        game.gamedata[first_name] = Object.assign({}, playerScoreTemplate);
                    }
                    heartbeat_error = 0;
                } else {
                    heartbeat_error++;
                }
            })
        })
        .catch(() => {
            heartbeat_error++;
            if (heartbeat_error > 2) {
                let lobby_error = document.getElementById('lobby-error');
                let lobby_error_content = document.getElementById('lobby-error-content');
                lobby_error_content.innerHTML = "Verbindung unterbrochen. Zu lange keine Verbindung zur Lobby beibehalten. Leite zurück zur Lobbyliste.";
                lobby_error.hidden = false;
                lobby_error.classList.remove('invisible');
                setTimeout(() => {
                    window.location.href = base_url + '/lobbylist';
                }, 5000);
            }
        });
    fetch(api_url + '/lobbyuser/?lkey=' + lobby_key)
        .then(data => data.json()
            .then(json => {
                const table_body = document.getElementById('table-body');
                let cleared = false;
                playeramount.innerHTML = json.length;

                let allReady = true;
                let hasAnswer = false;

                for (let i = 0; i < json.length; i++) {
                    let lobbyuser = json[i];
                    let player_name = lobbyuser.first_name;
                    let ready = lobbyuser.LPready;

                    if (!ready)
                        allReady = false;
                    hasAnswer = true;

                    // Create children
                    let row = document.createElement('tr');

                    let row_name = document.createElement('td');
                    let row_ready = document.createElement('td');

                    // Fill data
                    row_name.innerHTML = player_name;
                    row_ready.innerHTML = ready ? 'Bereit' : 'Nicht bereit';

                    // Set design
                    if (player_name === first_name)
                        row.classList.add('table-info');
                    else if (ready)
                        row.classList.add('table-success');
                    else
                        row.classList.add('table-danger');

                    row_ready.classList.add('text-center');

                    // Append children
                    row.appendChild(row_name);
                    row.appendChild(row_ready);

                    if (!cleared) {
                        table_body.innerHTML = "";
                        cleared = true;
                    }
                    table_body.appendChild(row);
                }

                if (allReady && hasAnswer) {
                    button_ready.disabled = true;
                    prepGame();
                }
            }));
}, 250);

function stopHeartbeat() {
    clearInterval(heartbeat);
}

function fetchLobbyData() {
    fetch(api_url + '/lobbydata/?lkey=' + lobby_key)
        .then(data => data.json()
            .then(json => {
                if (json.length < 1)
                    return;

                let lobby = json[0];
                game.meta.timePerQuestion = parseInt(lobby.Ltimeamount);
                game.meta.maxQuestions = parseInt(lobby.Lquestionamount);


                //'Lkey', 'Lname', 'Ltype', 'Lplayerlimit', 'Lquestionamount', 'Ltimeamount', 'LcurrentQuestion', 'LcurrentCorrect' //todo
            }));
}

function fetchQuestions() {
    fetch(api_url + '/questiontype/')
        .then(data => data.json()
            .then(json => {
                for (let i = 0; i < json.length; i++) {
                    game.meta.qTypes.addQuestionType(parseInt(json[i].QTid), json[i].QTname, json[i].QTdescription);
                }
            }));

    fetch(api_url + '/lobbyquestions/?lkey=' + lobby_key)
        .then(data => data.json()
            .then(json => {
                game.meta.maxQuestions = json.length;
                for (let i = 0; i < json.length; i++) {
                    let qid = json[i].Qid;

                    fetch(api_url + '/question/?qid=' + qid)
                        .then(qData => qData.json()
                            .then(qJson => {

                                encrypt(qJson[0].Qtext, lobby_key)
                                    .then(cryptQ => {
                                        let question = document.createElement('meta');

                                        question.id = 'question-' + i;
                                        question.classList.add('question-data');
                                        question.setAttribute('data-qid', qid);
                                        question.setAttribute('data-cid', qJson[0].Cid);
                                        question.setAttribute('data-cname', qJson[0].Cname);
                                        //question.setAttribute('data-qtext', qJson[0].Qtext);
                                        question.setAttribute('data-qtext', cryptQ);
                                        question.setAttribute('data-qtype', qJson[0].QTid);
                                        question_data.appendChild(question);

                                        fetch(api_url + '/answer/?qid=' + qid)
                                            .then(aData => aData.json()
                                                .then(aJson => {
                                                    for (let j = 0; j < aJson.length; j++) {

                                                        encrypt(aJson[j].Atext, lobby_key)
                                                            .then(cryptA => {
                                                                let answer = document.createElement('meta');

                                                                answer.id = 'answer-' + i + '-' + j;
                                                                answer.classList.add('answer-data');
                                                                answer.classList.add('answer-question-' + i);
                                                                answer.setAttribute('data-qid', qid);
                                                                answer.setAttribute('data-anum', aJson[j].Anum);
                                                                //answer.setAttribute('data-atext', aJson[j].Atext);
                                                                answer.setAttribute('data-atext', cryptA);

                                                                answer_data.appendChild(answer);
                                                            });

                                                    }
                                                }));
                                    });

                            }));

                }
            }));
}

setTimeout(fetchLobbyData, 100);
setTimeout(fetchQuestions, 200);