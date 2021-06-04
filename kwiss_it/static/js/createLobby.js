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
let maxpage = 1;
let page = 1;
let pages = new Set();
let prevpage = 1;

function toggle_page(pagereq, on) {
    let rows = document.getElementsByClassName(pagereq.toString())
    let descrows = document.getElementsByClassName("desc"+pagereq.toString())
    for (let i = 0; i < rows.length; i++) {
        if (on) {
            rows[i].setAttribute("hidden", "true");

        } else {
            rows[i].removeAttribute("hidden");
        }
    }
    for (let i = 0; i< descrows.length; i++){
        descrows[i].setAttribute("hidden", "true");
    }
}
function show_desc(id){
    let desc = document.getElementById(id);
    desc.hidden = false;
}

function reloadCategory(reqpage = 1) {
    if (reqpage>maxpage){
        reqpage=maxpage;
    } else if (reqpage <1){
        reqpage = 1;
    }
    let url= api_url+ "/category/?page="+reqpage
    if (!pages.has(reqpage)) {
        fetch(url)
            .then(data => data.json()
                .then(json => {
                    if (maxpage == null) {
                        if (json.count % 10 != 0) {
                            maxpage = (json.count - (json.count % 10)) / 10 + 1;

                        } else {
                            maxpage = (json.count - (json.count % 10)) / 10
                        }
                    }
                    if (json.results.length > 0) {
                        let table = document.getElementById("categorylist");
                        toggle_page(prevpage, false);
                        for (let i = 0; i < json.results.length; i++) {
                            let category = json.results[i];

                            let row_content = document.createElement("tr");
                            let row_desc = document.createElement("tr");

                            row_content.classList.add(reqpage.toString());
                            row_desc.classList.add("desc" + reqpage.toString());
                            row_content.setAttribute("for_desc", "cat" + category.Cid.toString());
                            row_desc.id = "cat" + category.Cid.toString();
                            row_desc.hidden = true;

                            let category_name = document.createElement("td");
                            let category_qa = document.createElement("td");
                            let category_choose = document.createElement("td");
                            category_name.innerText = category.Cname;
                            category_qa.innerText = "TODO"; //TODO add question amount to api

                            let chk_choose = document.createElement("input");
                            chk_choose.type = "checkbox";
                            chk_choose.name = "categories";
                            chk_choose.classList.add("form-check-input");
                            chk_choose.value = category.Cid.toString();
                            category_choose.appendChild(category_choose);

                            row_content.appendChild(category_name);
                            row_content.appendChild(category_qa);
                            row_content.appendChild(category_choose);

                            let td_desc = document.createElement("td");
                            td_desc.setAttribute("colspan", "3");
                            td_desc.innerText = category.Cdescription;
                            row_desc.appendChild(td_desc);

                            row_content.addEventListener("click", () => {
                                show_desc(row_content.for_desc)
                            })
                            table.appendChild(row_content);
                            table.appendChild(row_desc);

                        }
                        pages.add(reqpage)
                        prevpage = reqpage;
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
        toggle_page(prevpage, false)
        toggle_page(reqpage, true)
        prevpage = reqpage;
    }
}

function nextPage() {
    if (page >= maxpage) {
        page = maxpage;
    } else {
        page += 1;
        reloadCategory(page);
    }
}

function prevPage() {
    if (page <= 0) {
        page = 0;
    } else {
        page -= 1;
        reloadCategory(page)
    }
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
    reloadCategory(1)
}