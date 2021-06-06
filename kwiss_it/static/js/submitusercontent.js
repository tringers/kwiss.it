/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

let catselect = document.getElementById("category");
let divcreatecategory = document.getElementById("createcat");
let questionamount = document.getElementById("questionamount");
let addquestion = document.getElementById("addquestion");
let divquestions = document.getElementById("questions");
let template;
let answertemplate;
let questionsset = new Set();
let maxquestion = 0;
let questiontypes = JSON;

function start() {
    getTemplate();
    categorylist();
    getquestiontypes();
}

function categorylist(url = api_url + "/category/?approved=true&pending=true") {
    fetch(url)
        .then(data => data.json()
            .then(json => {
                let next = json.next;
                let content = json.results
                if (!content) {
                    return
                }
                for (let i = 0; i < content.length; i++) {
                    let catoption = document.createElement("option")
                    catoption.value = content[i].Cid;
                    catoption.innerText = content[i].Cname;
                    catselect.appendChild(catoption)
                }
                if (next != null) {
                    categorylist(next)
                }

            })
        );
}

function getquestiontypes() {
    url = api_url + "/questiontype/"
    fetch(url)
        .then(data => data.json()
            .then(json => {
                questiontypes = json
            })
        );
}

function getTemplate() {
    let temp = document.getElementById("template");
    template = temp.innerHTML;
    temp.remove()
    let temp2 = document.getElementById("templateanswer");
    answertemplate = temp2.innerHTML;
    temp2.remove()
}


function faddquestion() {
    maxquestion += 1;
    questionsset.add(maxquestion)
    let divquestion = document.createElement("div");
    divquestion.id = "q" + maxquestion.toString();
    divquestion.innerHTML = template;
    divquestion.classList.add("border", "row", "col-lg-8", "mx-auto", "p-3")
    divquestions.appendChild(divquestion)


    let questionNumber = document.getElementById("questionnumber");
    let questionNumberField = document.getElementById("questionnumberfield");
    let qtype = document.getElementById("qtype");
    let answeramount = document.getElementById("answeramount");
    let answeramountfield = document.getElementById("answeramountfield");
    let questiontext = document.getElementById("questiontext");
    let answers = document.getElementById("answers");
    let removequestion = document.getElementById("removequestion");

    questionNumber.innerText = "Frage Nummer " + maxquestion.toString();
    questionNumber.id = "questionnumber" + maxquestion.toString();
    questionNumber.name = "questionnumber" + maxquestion.toString();

    questionNumberField.id = "questionnumberfield" + maxquestion.toString();
    questionNumberField.name = "questionnumberfield";
    questionNumberField.value = maxquestion.toString();


    for (let i = 0; i < questiontypes.length; i++) {
        let option = document.createElement("option");
        option.value = questiontypes[i].QTname;
        option.innerText = questiontypes[i].QTdescription
        qtype.appendChild(option)
    }
    qtype.id = "qtype" + maxquestion.toString();
    qtype.name = "qtype" + maxquestion.toString();
    qtype.addEventListener("change", function () {
        if (qtype.value == "single" || qtype.value == "multiple") {
            answeramount.removeAttribute("hidden")
            answeramountfield.value = answeramount.value;
        } else {
            answeramount.setAttribute("hidden", "true");
            answeramountfield.value = "1";
        }
        answeramountfield.dispatchEvent(new Event("change"))
    });
    answeramount.id = "answeramount" + maxquestion.toString();
    if (qtype.value == "single" || qtype.value == "multiple") {
        answeramount.removeAttribute("hidden")
        answeramountfield.value = answeramount.value;

    } else {
        answeramount.setAttribute("hidden", "true");
        answeramountfield.value = "1";
    }
    answeramount.addEventListener("change", function () {
        answeramountfield.value = answeramount.value;
        answeramountfield.dispatchEvent(new Event("change"))
    })
    answeramountfield.addEventListener("change", function () {

        answers.innerHTML = "";
        let amount = parseInt(answeramountfield.value);
        for (let i = 0; i < amount; i++) {
            let divanswer = document.createElement("div");
            divanswer.innerHTML = answertemplate;
            answers.appendChild(divanswer);
            divanswer.id = "question" + maxquestion.toString() + "answer" + i.toString();
            divanswer.classList.add("border", "row", "col-lg-10", "mx-auto", "p-3", "rounded");

            let answernumber = document.getElementById("answernumber");
            let answernumberfield = document.getElementById("answernumberfield");
            let answertext = document.getElementById("answertext");
            let correct = document.getElementById("correct");
            let correctdiv = document.getElementById("correctdiv");

            answernumber.innerText = "Antwort " + (i + 1).toString();
            answernumber.id = "question" + maxquestion.toString() + "answernumber" + i.toString()
            answernumberfield.id = "question" + maxquestion.toString() + "answernumberfield" + i.toString()
            answernumberfield.name = "question" + maxquestion.toString() + "answernumberfield" + i.toString()
            answernumberfield.value = i.toString();
            answertext.id = "question" + maxquestion.toString() + "answertext" + i.toString();
            answertext.name = "question" + maxquestion.toString() + "answertext" + i.toString();
            correctdiv.id = "question" + maxquestion.toString() + "correctdiv" + i.toString();

            correct.id = "question" + maxquestion.toString() + "correct" + i.toString();
            correct.value = i.toString();
            if (qtype.value == "multiple") {
                correct.name = "question" + maxquestion.toString() + "correct" + i.toString();
            } else if (qtype.value == "number_exact" | qtype.value == "number_deviation") {
                correct.name = "question" + maxquestion.toString() + "correct";
                correct.type = "radio";
                correct.setAttribute("checked", "true")
                correctdiv.setAttribute("hidden", "true");
                answertext.type = "number"
            } else {
                correct.name = "question" + maxquestion.toString() + "correct";
                correct.type = "radio";

                correct.setAttribute("checked", "true");

            }
        }

    })
    answers.id = "answers" + maxquestion.toString();
    answeramountfield.dispatchEvent(new Event("change"))
    answeramountfield.id = "answeramountfield" + maxquestion.toString();
    answeramountfield.name = "answeramountfield" + maxquestion.toString();
    questiontext.id = "questiontext" + maxquestion.toString();
    questiontext.name = "questiontext" + maxquestion.toString();
    removequestion.id = "removequestion" + maxquestion.toString();
    removequestion.addEventListener("click", function () {
        questionsset.delete(divquestion.id.replace("q", ""))
        questionamount.value = questionsset.size.toString()
        divquestion.remove()
    })
    questionamount.value = questionsset.size.toString()

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