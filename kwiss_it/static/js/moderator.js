/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */
const cattemplate = document.getElementById("templateaccordionitemclass");
const qtemplate = document.getElementById("templateaccordionitemquestion");
const atemplate = document.getElementById("templateanswer");

const accordioncat = document.getElementById("accordioncat")

function start() {
    categorylist()
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
                    divcat.innerHTML=cattemplate.innerHTML;
                    divcat.classList.add("accordion-item");
                    accordioncat.appendChild(divcat);

                    let accordionheader = document.getElementById("accordionheader")
                    let collapseOne = document.getElementById("collapseOne")
                    accordionheader.id="accordionheader"+i.toString();
                    accordionheader.setAttribute("data-bs-target","collapseOne"+i.toString());
                    collapseOne.id="collapseOne"+i.toString();


                    let catname = document.getElementById("catname")
                    let catdesc = document.getElementById("catdesc")
                    let catstate = document.getElementById("catstate")
                    let btnpromote = document.getElementById("promote")
                    let btndemote = document.getElementById("demote")

                    catname.innerText= content[i].Cname;
                    catname.id="catname"+i.toString();
                    catdesc.innerText= content[i].Cdescription;
                    catdesc.id="catdesc"+i.toString();
                    catstate.innerText= (content[i].STid == 1)? "approved" : (content[i].STid == 2)? "pending" : "denied";
                    catstate.id="catstate"+i.toString();
                    btnpromote.value=(content[i].STid == 1)? "pending" : "approved";
                    btnpromote.id="promote"+i.toString();
                    btndemote.value=(content[i].STid == 3)? "pending" : "denied" ;

                    btnpromote.addEventListener("click",function (){

                    })
                    btndemote.addEventListener("click",function (){

                    })

                    let accordionquestions = document.getElementById("accordionquestions")
                    accordionquestions.id="accordionquestions"+i.toString();
                    addquestion(i.toString())

                }
                if (next != null) {
                    categorylist(next)
                }

            })
        );
}

function addquestion(i) {
    let accordionquestions = document.getElementById("accordionquestions"+i)
    let divquestion= document.createElement("div")
    divquestion.classList.add("accordion-item");
    divquestion.innerHTML= qtemplate.innerHTML;
    accordionquestions.appendChild(divquestion)



}


document.addEventListener("DOMContentLoaded", start);
