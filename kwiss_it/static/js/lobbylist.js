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
                    let row = document.createElement('tr');

                    let lobby_private = document.createElement('td');
                    let lobby_name = document.createElement('td');
                    let lobby_player = document.createElement('td');
                    let lobby_mode = document.createElement('td');
                    let lobby_join = document.createElement('td');
                    let lobby_join_button = null;

                    if(lobby.Lprivate) {
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

                    lobby_private.innerHTML = lobby.Lprivate ? '&#128274' : '';
                    lobby_name.innerHTML = lobby.Lname;
                    // TODO: Count player per lobby
                    lobby_player.innerHTML = '0 / ' + lobby.Lplayerlimit;
                    lobby_mode.innerHTML = list_lobbytype[lobby.Ltype] ? list_lobbytype[lobby.Ltype] : lobby.Ltype;
                    lobby_join.appendChild(lobby_join_button);

                    row.appendChild(lobby_private);
                    row.appendChild(lobby_name);
                    row.appendChild(lobby_player);
                    row.appendChild(lobby_mode);
                    row.appendChild(lobby_join);
                    table_body.appendChild(row);
                }
            })
            .catch(e => {
                // Error parsing data to json
            }))
        .catch(e => {
            // Error fetching data from api
        });
}