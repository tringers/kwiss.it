// Get Lobbytypes first
list_lobbytype = [];

fetch(api_url + '/lobbytype/')
    .then(data => data.json()
        .then(json => {
            for (let i = 0; i < json.length; i++) {
                let lobbytype = json[i];
                let id = parseInt(lobbytype.LTid);
                list_lobbytype[id] = lobbytype.LTdescription;
            }
            getLobbys();
        })
        .catch(e => {
            // Error parsing data to json
        }))
    .catch(e => {
        // Error fetching data from api
    });

function getLobbys() {
    fetch(api_url + '/lobby/')
        .then(data => data.json()
            .then(json => {
                    let table_body = document.getElementById('table-body');

                    for (let i = 0; i < json.length; i++) {
                        let lobby = json[i];

                        // Get all player in lobby for counting
                        fetch(api_url + '/lobbyuser/?lkey=' + lobby.Lkey)
                            .then(cData => cData.json()
                                .then(cJson => {

                                    let row = document.createElement('tr');

                                    let lobby_private = document.createElement('td');
                                    let lobby_name = document.createElement('td');
                                    let lobby_user = document.createElement('td');
                                    let lobby_mode = document.createElement('td');
                                    let lobby_join = document.createElement('td');
                                    let lobby_join_button = null;

                                    lobby_private.innerHTML = lobby.Lprivate ? '&#128274' : '';
                                    lobby_name.innerHTML = lobby.Lname;

                                    lobby_user.innerHTML = cJson.length + ' / ' + lobby.Lplayerlimit;
                                    lobby_mode.innerHTML = list_lobbytype[lobby.Ltype] ? list_lobbytype[lobby.Ltype] : lobby.Ltype;

                                    if (lobby.Lprivate) {
                                        // If private Lobby, Button opens inputPassword window
                                        lobby_join_button = document.createElement('button');
                                        lobby_join_button.innerHTML = 'Beitreten';
                                        //lobby_join_button.href = '/lobby/' + lobby.Lkey + '/';
                                        lobby_join_button.classList.add('btn');
                                        lobby_join_button.classList.add('btn-outline-primary');
                                        lobby_join_button.classList.add('btn-sm');
                                        lobby_join_button.classList.add('col-12');
                                        lobby_join_button.setAttribute('role', 'button');
                                        lobby_join_button.setAttribute('data-bs-toggle', 'modal');
                                        lobby_join_button.setAttribute('data-bs-target', '#joinPrivate');
                                        lobby_join_button.addEventListener('click', () => {
                                            let passwd = document.getElementById('joinPrivate');
                                            passwd.setAttribute('data-lobbykey', lobby.Lkey);
                                        });
                                    } else {
                                        // If public Lobby, Button is a redirect
                                        lobby_join_button = document.createElement('a');
                                        lobby_join_button.innerHTML = 'Beitreten';
                                        lobby_join_button.href = '/lobby/' + lobby.Lkey + '/';
                                        lobby_join_button.classList.add('btn');
                                        lobby_join_button.classList.add('btn-outline-primary');
                                        lobby_join_button.classList.add('btn-sm');
                                        lobby_join_button.classList.add('col-12');
                                        lobby_join_button.setAttribute('role', 'button');
                                    }

                                    if (cJson.length === lobby.Lplayerlimit) {
                                        lobby_join_button.disabled = true;
                                    }

                                    lobby_join.appendChild(lobby_join_button);

                                    row.appendChild(lobby_private);
                                    row.appendChild(lobby_name);
                                    row.appendChild(lobby_user);
                                    row.appendChild(lobby_mode);
                                    row.appendChild(lobby_join);
                                    table_body.appendChild(row);


                                }));
                    }
                }
            )
            .catch(e => {
                // Error parsing data to json
            }))
        .catch(e => {
            // Error fetching data from api
        });
}

let joinPrivate = document.getElementById('joinPrivate');
let inputLobbyPassword = document.getElementById('inputLobbyPassword');
let submitLobbyPassword = document.getElementById('submitLobbyPassword');
submitLobbyPassword.addEventListener('click', () => {
    let password = inputLobbyPassword.value;
    let lobby_key = joinPrivate.getAttribute('data-lobbykey');

    // Hash password
    digestMessage(password, 250000)
        .then((hexHash) => {
            // Send to server with Lobby Key
            window.location.href = base_url + '/lobby/' + lobby_key + '/?passhash=' + hexHash;
        });
});

async function digestMessage(message, count) {
    let hashArray = new TextEncoder().encode(message);
    for (let i = 0; i < count; i++) {
        const hashBuffer = await crypto.subtle.digest('SHA-256', hashArray);
        hashArray = Array.from(new Uint8Array(hashBuffer));
    }
    return hashArray.map(b => b.toString(16).padStart(2, '0')).join('');
}
