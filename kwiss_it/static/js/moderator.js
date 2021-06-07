/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */
let cattemplate = document.getElementById("templateaccordionitemclass").innerHTML;
let qtemplate = ""
let atemplate = ""

const accordioncat = document.getElementById("accordioncat")
let QTtype = new Map;

function start() {
    getTemplate()
    categorylist()
}

function getQuestionType() {
    fetch(api_url + "/questiontype")
        .then(data => data.json()
            .then(json => {
                for(let i=0;i<json.length;i++){
                    QTtype.set(json[i].QTid,json[i].QTdescription)
                }
            })
        );


}

function getTemplate() {
    let templatetempa = document.getElementById("templateanswer")
    atemplate = templatetempa.innerHTML;
    templatetempa.remove()

    let templatetempq = document.getElementById("templateaccordionitemquestion");
    qtemplate = templatetempq.innerHTML;
    templatetempq.remove();

    let templatetempc = document.getElementById("templateaccordionitemclass");
    cattemplate = templatetempc.innerHTML;
    templatetempc.remove();
    return
}


function categorylist(url = api_url + "/category/?approved=true&pending=true&denied=true") {
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let next = json.next;
                let content = json.results
                if (!content) {
                    return
                }
                for (let i = 0; i < content.length; i++) {
                    let divcat = document.createElement("div")
                    divcat.innerHTML = cattemplate;
                    divcat.classList.add("accordion-item");
                    accordioncat.appendChild(divcat);

                    let accordionheader = document.getElementById("accordionheader")
                    let collapseOne = document.getElementById("collapseOne")
                    accordionheader.id = "accordionheader" + i.toString();
                    accordionheader.setAttribute("data-bs-target", "#collapseOne" + i.toString());
                    collapseOne.id = "collapseOne" + i.toString();


                    let catname = document.getElementById("catname")
                    let catdesc = document.getElementById("catdesc")
                    let catstate = document.getElementById("catstate")
                    let btnpromote = document.getElementById("promote")
                    let btndemote = document.getElementById("demote")

                    catname.innerHTML = content[i].Cname;
                    catname.id = "catname" + i.toString();
                    catdesc.innerHTML = content[i].Cdescription;
                    catdesc.id = "catdesc" + i.toString();
                    catstate.innerHTML = (content[i].STid === 1) ? "approved" : (content[i].STid === 2) ? "denied" : "pending";
                    catstate.id = "catstate" + i.toString();
                    btnpromote.innerHTML = (content[i].STid === 1) ? "pending" : "approved";
                    btnpromote.id = "promote" + i.toString();
                    btndemote.innerHTML = (content[i].STid === 3) ? "pending" : "denied";

                    btnpromote.addEventListener("click", function () {

                    })
                    btndemote.addEventListener("click", function () {

                    })

                    let accordionquestions = document.getElementById("accordionquestions")
                    accordionquestions.id = "accordionquestions" + i.toString();
                    addquestion(i.toString(), content.Cid)

                }
                if (next != null) {
                    categorylist(next)
                }

            })
        );
}

function addquestion(i, cid) {

    url = api_url + "/question/?approved=true&pending=true&denied=true&cid=" + cid.toString()
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let accordionquestions = document.getElementById("accordionquestions" + i)
                let divquestion = document.createElement("div")
                divquestion.classList.add("accordion-item");
                divquestion.innerHTML = qtemplate;
                accordionquestions.appendChild(divquestion)

                for (let a = 0; a < json.length; a++) {
                    let tdquestion = document.getElementById("question")
                    let tdquestiontype = document.getElementById("questiontype")
                    let tdquestionstate = document.getElementById("questionstate")
                    let btnqpromote = document.getElementById("qpromote")
                    let btnqdemote = document.getElementById("qdemote")

                    tdquestion.id = "category"+i+"question"+a.toString();
                    tdquestion.innerHTML = json[a].Qtext;
                    tdquestiontype.id = "category"+i+"questiontype"+a.toString();
                    tdquestiontype.innerHTML= QTtype.get(json[a].QTid);
                    tdquestionstate.id="category"+i+"questionstate"+a.toString();
                    tdquestionstate.innerHTML= (json[a].STid === 1) ? "approved" : (json[a].STid === 2) ? "denied" : "pending";

                    btnqpromote.id = "category"+i+"qpromote"+a.toString();
                    btnqpromote.innerHTML= (json[a].STid === 1) ? "pending" : "approved";
                    btnqdemote.id = "category"+i+"qdemote"+a.toString();
                    btnqdemote.innerHTML = (json[a].STid === 3) ? "pending" : "denied";

                    let answers = document.getElementById("answers")
                    answers.id="category"+i+"answers"+a.toString();
                    addanswers(i,a)
                }
            })
        );

}

function addanswers(i, q) {

}

document.addEventListener("DOMContentLoaded", start);
