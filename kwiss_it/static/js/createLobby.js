/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

const qamin = 5;    //questionamountmin
const qamax = 50;   //questionamountmax
const tamin = 10;  //timeamountmin
const tamax = 124; //timeamountmax
const pamin = 2;    //playeramountmin
const pamax = 30;   //playeramountmax

const tbody = document.getElementById('categorylist');
const cat_selects = document.getElementById('categorySelects');
const lobbytype = document.getElementById("lobbytype");
let current_page = 1;
let max_page = 1;
let categories = {};

function fetchCategory(pending = false, clear = false) {
    let fetch_param = '?approved=true' + (pending ? '&pending=true' : '');

    if (clear) {
        current_page = 1;
        categories = {};
    }

    // Get max page
    fetch(api_url + '/category/' + fetch_param + '&page=1')
        .then(pData => pData.json()
            .then(pJson => {
                max_page = Math.ceil(pJson.count / 10);

                fetch(api_url + '/category/' + fetch_param + '&page=' + current_page)
                    .then(data => data.json()
                        .then(json => {
                            for (let i = 0; i < json.results.length; i++) {
                                let cat = json.results[i];
                                if (categories[cat.Cname] === undefined)
                                    categories[cat.Cname] = cat;
                            }

                            refreshCategoryAmount();
                            refreshTable();
                        }));
            }));
}

function refreshCategoryAmount() {
    let cat_names = Object.keys(categories);

    for (let i = 0; i < cat_names.length; i++) {
        let category = categories[cat_names[i]];
        let url= api_url + '/question/?cid=' + category.Cid+"&approved=true"+(pending ? '&pending=true' : '');
        if(lobbytype.value == "single" || lobbytype.value =="Single"){
            url+="&single=1"
        }
        if (category.Camount === undefined) {
            fetch(url)
                .then(data => data.json()
                    .then(json => {
                        if (json === undefined || json === [] || json.length <= 0) {
                            categories[cat_names[i]].Camount = 0;
                            refreshTable();
                        } else {
                            categories[cat_names[i]].Camount = json.length;
                            refreshTable();
                        }
                    }));
        }
    }
}

function refreshTable() {
    // Sort
    categories = Object.keys(categories).sort().reduce(
        (obj, key) => {
            obj[key] = categories[key];
            return obj;
        },
        {}
    );

    let cat_names = Object.keys(categories);
    tbody.innerHTML = "";

    for (let i = (current_page - 1) * 10; i < Math.min(current_page * 10, cat_names.length); i++) {
        let category = categories[cat_names[i]];

        // Category data
        let row_data = document.createElement('tr');
        let data_name = document.createElement('td');
        let data_amount = document.createElement('td');
        let data_select = document.createElement('td');
        let data_select_checkbox = document.createElement("input");

        data_name.innerHTML = category.Cname;
        data_amount.innerHTML = category.Camount;
        data_amount.classList.add('text-center');
        data_select.classList.add('selection-hover');
        data_select.classList.add('text-center');

        data_select_checkbox.type = "checkbox";
        data_select_checkbox.name = "categories";
        data_select_checkbox.classList.add("form-check-input");
        data_select_checkbox.value = category.Cid.toString();

        if (category.selected === undefined) {
            category.selected = false;
            categories[cat_names[i]].selected = false;
        }

        data_select_checkbox.checked = category.selected;

        data_select_checkbox.addEventListener('click', (e) => {
            data_select_checkbox.checked = !data_select_checkbox.checked;
            categories[cat_names[i]].selected = data_select_checkbox.checked;
            updateCategorySelect();
        });
        data_select.addEventListener('click', (e) => {
            data_select_checkbox.checked = !data_select_checkbox.checked;
            categories[cat_names[i]].selected = data_select_checkbox.checked;
            updateCategorySelect();
        });

        data_select_checkbox.addEventListener('change', () => {
            categories[cat_names[i]].selected = data_select_checkbox.checked;
            updateCategorySelect();
        });

        data_select.appendChild(data_select_checkbox);

        row_data.appendChild(data_name);
        row_data.appendChild(data_amount);
        row_data.appendChild(data_select);

        tbody.appendChild(row_data);

        // Category description
        let row_description = document.createElement('tr');
        let data_description = document.createElement('td');

        row_description.hidden = true;
        data_description.setAttribute("colspan", "3");
        data_description.innerText = category.Cdescription;

        row_description.appendChild(data_description);

        tbody.appendChild(row_description);

        data_name.addEventListener("click", (e) => {
            row_description.hidden = !row_description.hidden;
        });
        data_amount.addEventListener("click", (e) => {
            row_description.hidden = !row_description.hidden;
        });

        let row_filler = document.createElement("tr");
        row_filler.hidden = true;
        tbody.appendChild(row_filler);
    }
}

function updateCategorySelect() {
    let cat_names = Object.keys(categories);
    cat_selects.innerHTML = "";

    for (let i = 0; i < cat_names.length; i++) {
        let checkbox = document.createElement("input");
        checkbox.value = categories[cat_names[i]].Cid.toString();
        checkbox.checked = categories[cat_names[i]].selected;
        cat_selects.appendChild(checkbox)
    }
}

fetchCategory();

document.getElementById('prev').addEventListener('click', () => {
    current_page--;
    if (current_page < 1)
        current_page = 1;
    fetchCategory();
});

document.getElementById('next').addEventListener('click', () => {
    current_page++;
    if (current_page > max_page)
        current_page = max_page;
    fetchCategory();
});



let lobbypasswordfield = document.getElementById("lobbypasswordfield");

let lobbynamefield= document.getElementById("lobbynamefield");
let createlobbyname= document.getElementById("createlobbyname");

let playeramountfielddiv= document.getElementById("playeramountfielddiv");

let gamerace = document.getElementById("gamerace");
let gamebasic = document.getElementById("gamebasic");
function publiclobby() {
    lobbypasswordfield.hidden = true;
    lobbynamefield.hidden = false;
    playeramountfielddiv.hidden=false;

    gamerace.removeAttribute("disabled")
}

function privatelobby() {
    lobbypasswordfield.hidden = false;
    lobbynamefield.hidden = false;
    playeramountfielddiv.hidden=false;

    gamerace.removeAttribute("disabled")
}
function singlelobby(){
    lobbypasswordfield.hidden = true;
    lobbynamefield.hidden = true;
    createlobbyname.value="";
    playeramountfielddiv.setAttribute("hidden","true");
    if (pending.checked) {
        refreshCategoryAmount()
    } else {
        refreshCategoryAmount()
    }
    gamerace.setAttribute("disabled","true")
    gamebasic.checked=true;
}


lobbytype.addEventListener("change", function () {
    if (lobbytype.value === "Öffentlich" || lobbytype.value === 'public') {
        publiclobby();
    } else if (lobbytype.value === "Privat" || lobbytype.value === 'private') {
        privatelobby();
    }else if(lobbytype.value === "Single"||lobbytype.value === "single"){
        singlelobby();
    }
});

//questionamount
let qaslider = document.getElementById("questionamountslider");
let qafield = document.getElementById("questionamountfield");
addSliderListener(qaslider, qafield, qamin, qamax);

//timeamount
let taslider = document.getElementById("timeamountslider");
let tafield = document.getElementById("timeamountfield");
addSliderListener(taslider, tafield, tamin, tamax);

//playeramount
let paslider = document.getElementById("playeramountslider");
let pafield = document.getElementById("playeramountfield");
addSliderListener(paslider, pafield, pamin, pamax);

function addSliderListener(slider, field, min, max) {
    let equalize = function (value) {
        value = Math.min(value, max);
        value = Math.max(value, min);
        slider.value = value;
        field.value = value;
    }

    slider.addEventListener("change", () => {
        equalize(slider.value);
    });
    field.addEventListener("change", () => {
        equalize(field.value);
    });
}

let pending = document.getElementById("pending");
pending.addEventListener("change", function () {
    if (pending.checked) {
        fetchCategory(true, false);
    } else {
        fetchCategory(false, true);
    }
});