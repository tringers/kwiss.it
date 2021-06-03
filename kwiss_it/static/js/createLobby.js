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
    let xhttp = new XMLHttpRequest();
    let url=""
    if (lastcat != "") {
        url = "/api/category/?lastcat=" + lastcat;
    } else {
        url = "/api/category/";
    }
    xhttp.open("GET", url, true);
    xhttp.responseType = "json";
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            let table = document.getElementById("categorylist");
            let content = JSON.parse(this.responseText);
            let tableNew = "";
            for (let i = 0; i < content.entries.length; i++) {
                tableNew += "<tr> <td>" + content.entries[i].Cname + "</td>" +
                    " <td> TODO </td>" +
                    " <td> <input class=\"form-check-input\" type=\"checkbox\" name=\"categorys\" value=\"" + content.entries[i].STid + "\"> </td> </tr>";
            }
            table.innerHTML = tableNew;
            let length= content.entries.length;
            if (length >= 1) {
                currentCategory = content.entries[length-1].Cname;
            }
        }
    }
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
    let intervalId = setInterval(() => {reloadScoreboard(currentCategory)},2000);
}