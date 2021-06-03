/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

const qamax = 50;   //questionamountmax
const qamin = 5;    //questionamountmin
const tamin = 10;  //timeamountmin
const tamax = 124; //timeamountmax
const pamin = 2;    //playeramountmin
const pamax = 16;   //playeramountmax
let lastCategory = ""; //last loaded category
let currentCategory = ""; //current viewing category
function reloadScoreboard(lastcat = "") {
    let url = ""
    if (lastcat !== "") {
        url = "/api/category/?lastcat=" + lastcat;
    } else {
        url = "/api/category/";
    }
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let table = document.getElementById("categorylist");
                for (let i = 0; i < json.length; i++) {
                    let category = json[i];
                    let row = document.createElement('tr');
                    let category_name = document.createElement('td');
                    let category_question_amount = document.createElement('td');
                    let category_add_field = document.createElement('td');
                    let category_add = document.createElement('input')

                    category_name.innerHTML = category.Cname;
                    category_question_amount.innerHTML = "TODO"; //TODO add question amount of category
                    category_add.classList.add('form-check-input');
                    category_add.type = 'checkbox';
                    category_add.name = 'categorys';
                    category_add.value = category.STid;

                    category_add_field.appendChild(category_add);

                    row.appendChild(category_name);
                    row.appendChild(category_question_amount);
                    row.appendChild(category_add_field);

                    table.appendChild(row);
                }
                if (json.length >= 1) {
                    currentCategory = lastCategory;
                    lastCategory = content.entries[json.length - 1].Cname;
                } else if (json.length == 0) {
                    lastCategory = currentCategory;
                }
            })
            .catch(e => {
                // Error parsing data to json
            }))
        .catch(e => {
            // Error fetching data from api
        });
}

let lobbytype = document.getElementById("lobbytype");
let lobbypasswordfield = document.getElementById("lobbypasswordfield");

function publiclobby() {
    lobbypasswordfield.hidden = true;
}

function privatelobby() {
    lobbypasswordfield.hidden = false;
}

lobbytype.addEventListener("change", function () {
    if (lobbytype.value === "Öffentlich" || lobbytype.value === 'public') {
        publiclobby();
    } else if (lobbytype.value === "Privat" || lobbytype.value === 'private') {
        privatelobby();
    }
});

//questionamount
let qaslider = document.getElementById("questionamountslider");
let qafield = document.getElementById("questionamountfield");
qaslider.addEventListener("change", function () {
    qafield.value = qaslider.value;
});
qafield.addEventListener("change", function () {
    if (qafield.value > qamax) {
        qafield.value = qamax;
    } else if (qafield.value < qamin) {
        qafield.value = qamin;
    }
    qaslider.value = qafield.value;
});
//timeamount
let taslider = document.getElementById("timeamountslider");
let tafield = document.getElementById("timeamountfield");
taslider.addEventListener("change", function () {
    tafield.value = taslider.value;
});
tafield.addEventListener("change", function () {
    if (tafield.value > tamax) {
        tafield.value = tamax;
    } else if (tafield.value < tamin) {
        tafield.value = tamin;
    }
    taslider.value = tafield.value;
});

//playeramount
let paslider = document.getElementById("playeramountslider");
let pafield = document.getElementById("playeramountfield");
paslider.addEventListener("change", function () {
    pafield.value = paslider.value;
});
pafield.addEventListener("change", function () {
    if (pafield.value > pamax) {
        pafield.value = pamax;
    } else if (pafield.value < pamin) {
        pafield.value = pamin;
    }
    paslider.value = pafield.value;
});


if (document.getElementById("categorylist")) {
    reloadScoreboard(currentCategory)
}