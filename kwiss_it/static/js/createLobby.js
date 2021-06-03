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
let maxpage = 1000;
let page = 0;
let categoryPages = new Map();
let prevpage = 0;

function toggle_list(list, on) {
    console.log(list)
    for (let i = 0; i < list.length; ++i) {
        list[i].style.display = on ? '' : 'none';

    }
}

let btnArray = new Array(5);
btnArray[0] = document.getElementById("1");
btnArray[1] = document.getElementById("2");
btnArray[2] = document.getElementById("3");
btnArray[3] = document.getElementById("4");
btnArray[4] = document.getElementById("5");
for (let btn of btnArray) {
    btn.addEventListener("click", () => {
        loadPage(btn.value - 1);
    })
}

function renumberButtons() {
    posArray = new Array(5);
    posArray[0] = page <= 3 ? 1 : page - 2;
    posArray[1] = page <= 3 ? 2 : page - 1;
    posArray[2] = page <= 3 ? 3 : page;
    posArray[3] = page <= 3 ? 4 : page + 1;
    posArray[4] = page <= 3 ? 5 : page + 2;
    for(let i= 0 ; i<5;i++){
        btnArray[i].value=posArray[i];
        btnArray[i].innerHTML=posArray[i];
    }

}

function reloadScoreboard(reqpage = 0) {


    let url = "/api/category/?page=" + reqpage;
    let content = categoryPages.get(reqpage);
    console.log(categoryPages);
    if (content == undefined) {
        fetch(url)
            .then(data => data.json()
                .then(json => {
                    if (json.length<15){
                        maxpage=reqpage;
                    }
                    if (json.length > 0) {
                        let table = document.getElementById("categorylist");
                        toggle_list(categoryPages.get(prevpage)|[],false);
                        pagerows= new Set();
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
                            category_add_field.appendChild(category_add);
                            row.classList.add(reqpage.toString())
                            row.appendChild(category_name);
                            row.appendChild(category_question_amount);
                            row.appendChild(category_add_field);

                            table.appendChild(row);
                            pagerows.add(row);
                        }
                        categoryPages.set(reqpage, pagerows)
                        prevpage = reqpage;
                        renumberButtons();
                    } else {
                        page = prevpage;

                    }

                })
                .catch(e => {
                    // Error parsing data to json
                }))
            .catch(e => {
                // Error fetching data from api
            });
    } else {
        toggle_list(categoryPages.get(prevpage)|[],false)
        toggle_list(categoryPages.get(reqpage)|[],true)
        prevpage = reqpage;
        renumberButtons();
    }
}

function nextPage() {
    if (page >= maxpage) {
        page = maxpage;
    } else {
        page += 1;
        reloadScoreboard(page);
    }
}

function prevPage() {
    if (page <= 0) {
        page = 0;
    } else {
        page -= 1;
        reloadScoreboard(page)
    }
}

function loadPage(clickedPage) {
    if (clickedPage >= maxpage) {
        page = maxpage;
    } else if (clickedPage <= 0) {
        page = 0;
    } else {
        page = clickedPage;
    }
    reloadScoreboard(page)
}

document.getElementById("prev").addEventListener("click", prevPage)
document.getElementById("next").addEventListener("click", nextPage)


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
    reloadScoreboard(0)
}