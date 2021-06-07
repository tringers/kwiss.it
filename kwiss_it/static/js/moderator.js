/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */
let cattemplate = ""
let qtemplate = ""
let atemplate = ""

const accordioncat = document.getElementById("accordioncat")
let QTtype = new Map;

function start() {
    getQuestionType()
    getTemplate()
    categorylist()
}

function getQuestionType() {
    fetch(api_url + "/questiontype")
        .then(data => data.json()
            .then(json => {
                for (let i = 0; i < json.length; i++) {
                    QTtype.set(json[i].QTid, json[i].QTdescription)
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
                    btnpromote.value = (content[i].STid === 1) ? "approved" : (content[i].STid === 2) ? "denied" : "pending";
                    btndemote.value = (content[i].STid === 1) ? "approved" : (content[i].STid === 2) ? "denied" : "pending";

                    btnpromote.addEventListener("click", (e) => {
                        stateEvent(e, "category",content[i].Cid)
                    });
                    btndemote.addEventListener("click", (e) => {
                        stateEvent(e, "category",content[i].Cid)
                    });

                    let accordionquestions = document.getElementById("accordionquestions")
                    accordionquestions.id = "accordionquestions" + i.toString();
                    addquestion(i.toString(), content[i].Cid)

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
                for (let q = 0; q < json.length; q++) {
                    let accordionquestions = document.getElementById("accordionquestions" + i)

                    let divquestion = document.createElement("div")
                    divquestion.classList.add("accordion-item");
                    divquestion.innerHTML = qtemplate;
                    accordionquestions.appendChild(divquestion)


                    let accordionheaderquestion = document.getElementById("accordionheaderquestion")
                    let collapseInner = document.getElementById("collapseInner")
                    accordionheaderquestion.id = "category" + i + "accordionheaderquestion" + q.toString();
                    accordionheaderquestion.setAttribute("data-bs-target", "#category" + i + "collapseInner" + q.toString())
                    collapseInner.id = "category" + i + "collapseInner" + q.toString();
                    collapseInner.setAttribute("data-bs-parent", "#accordionquestions" + i)

                    let tdquestion = document.getElementById("question")
                    let tdquestiontype = document.getElementById("questiontype")
                    let tdquestionstate = document.getElementById("questionstate")
                    let btnqpromote = document.getElementById("qpromote")
                    let btnqdemote = document.getElementById("qdemote")

                    tdquestion.id = "category" + i + "question" + q.toString();
                    tdquestion.innerHTML = json[q].Qtext;
                    tdquestiontype.id = "category" + i + "questiontype" + q.toString();
                    tdquestiontype.innerHTML = QTtype.get(json[q].QTid);
                    tdquestionstate.id = "category" + i + "questionstate" + q.toString();
                    tdquestionstate.innerHTML = (json[q].STid === 1) ? "approved" : (json[q].STid === 2) ? "denied" : "pending";

                    btnqpromote.id = "category" + i + "qpromote" + q.toString();
                    btnqpromote.innerHTML = (json[q].STid === 1) ? "pending" : "approved";
                    btnqpromote.value = (json[q].STid === 3) ? "pending" : "denied";
                    btnqdemote.id = "category" + i + "qdemote" + q.toString();
                    btnqdemote.innerHTML = (json[q].STid === 3) ? "pending" : "denied";
                    btnqdemote.value = (json[q].STid === 3) ? "pending" : "denied";

                    btnqpromote.addEventListener("click", (e) => {
                        stateEvent(e, "question",json[q].Qid)
                    });
                    btnqdemote.addEventListener("click", (e) => {
                        stateEvent(e, "question",json[q].Qid)
                    });

                    let answers = document.getElementById("answers")
                    answers.id = "category" + i + "answers" + q.toString();
                    addanswers(i, q.toString(), json[q].Qid);
                }
            })
        );
    return
}

function addanswers(i, q, qid) {
    let url = api_url + "/answer/?qid=" + qid.toString();
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let answers = document.getElementById("category" + i + "answers" + q);
                for (let a = 0; a < json.length; a++) {


                    let transwer = document.createElement("tr");
                    let answer = document.createElement("td");
                    let correct = document.createElement("td");

                    answer.id = "c" + i + "q" + q + "answer" + a.toString();
                    answer.innerHTML = json[a].Atext;
                    correct.id = "c" + i + "q" + q + "correct" + a.toString();

                    transwer.appendChild(answer)
                    transwer.appendChild(correct)
                    answers.appendChild(transwer);
                }

            })
        );

    return
}

function stateEvent(e, path, id) {
    e.disabled = true;
    let element = e.currentTarget;


    postState(base_url + '/state/' + path + '/' + id + '/' + element.value);
}

async function postState(url = '') {
    const response = await fetch(url, {
        method: 'POST',
        cache: 'no-cache',
        headers: {
            'Content-Type': 'application/json',
            "X-CSRFToken": document.getElementsByName('csrfmiddlewaretoken')[0].value,
        },
        credentials: 'same-origin',
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: "",
    });
    return response.json();
}


document.addEventListener("DOMContentLoaded", start);
