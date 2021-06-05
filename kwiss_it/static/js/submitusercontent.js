/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

let catselect = document.getElementById("category");
let divcreatecategory = document.getElementById("createcat");

let addquestion = document.getElementById("addquestion");
let divquestions = document.getElementById("questions");
let template;
let questionsset = new Set();
let maxquestion = 0;
let questiontypes = JSON;

function start() {
    getTemplate();
    categorylist();
    getquestiontypes();
}

function categorylist(url = api_url + "/category/") {
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let next=json.next;
                let content = json.content
                if (!content){
                    return
                }
                for(let i=0; i< content.length;i++){
                    let catoption = document.createElement("option")
                    catoption.value = content[i].Cid;
                    catoption.innerText = content[i].Cname;
                    catselect.appendChild(catoption)
                }
                if (next != null){
                    categorylist(next)
                }

            })
        );
}

function getquestiontypes() {

}

function getTemplate() {
    let temp = document.getElementById("template");
    template = temp.innerHTML;
    temp.innerHTML = "";
}

function faddquestion() {
    maxquestion += 1;
    let divquestion = document.createElement("div");
    divquestion.id = "q" + maxquestion.toString();
    divquestion.innerHTML = template;
    divquestion.classList.add("border")
    divquestions.appendChild(divquestion)


}


catselect.addEventListener("change", function () {
    if (catselect.value == "new") {
        divcreatecategory.removeAttribute("hidden")
    } else {
        divcreatecategory.setAttribute("hidden", "true")
    }
})

addquestion.addEventListener("click", faddquestion)

document.addEventListener("DOMContentLoaded", start);