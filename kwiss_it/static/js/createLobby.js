/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

const qamax = 64;
const qamin = 1;

function reloadScoreboard() {
    let xhttp = new XMLHttpRequest();
    let url = "" //TODO api url für kategorien einfügen
    xhttp.open("GET", url, true);
    xhttp.responseType = "json";
    xhttp.onload = function () {
        if (xhttp.status === 200) {
            let table = document.getElementById("categorylist");

        }
    }
}
let lobbytype = document.getElementById("lobbytype");
let lobbypasswordfield = document.getElementById("lobbypasswordfield");

function publiclobby() {
    lobbypasswordfield.hidden=true;
}

function privatelobby() {
    lobbypasswordfield.hidden=false;
}

lobbytype.addEventListener("change", function () {
    if (lobbytype.value == "Öffentlich") {
        publiclobby();
    } else if (lobbytype.value == "Privat") {
        privatelobby();
    }
});


let qaslider=document.getElementById("questionamountslider");
let qafield=document.getElementById("questionamountfield");
    qaslider.addEventListener("change",function(){
        qafield.value = qaslider.value;
    });
    qafield.addEventListener("change",function (){
        if(qafield.value> qamax){
            qafield.value=qamax;
        }else if(qafield.value < qamin){
            qafield.value=qamin;
        }
        qaslider.value = qafield.value;
    });
if (document.getElementById("categorylist")) {
    reloadScoreboard();
}