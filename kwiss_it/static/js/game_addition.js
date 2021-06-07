let qupvote = document.getElementById('question-upvote');
let qdownvote = document.getElementById('question-downvote');
let cupvote = document.getElementById('category-upvote');
let cdownvote = document.getElementById('category-downvote');

function resetVotebutton() {
    qupvote.disabled = false;
    qdownvote.disabled = false;
    cupvote.disabled = false;
    cdownvote.disabled = false;
}

qupvote.addEventListener('click', (e) => {
    voteEvent(e, 'question');
});
qdownvote.addEventListener('click', (e) => {
    voteEvent(e, 'question');
});
cupvote.addEventListener('click', (e) => {
    voteEvent(e, 'category');
});
cdownvote.addEventListener('click', (e) => {
    voteEvent(e, 'category');
});


function voteEvent(e, path) {
    e.disabled = true;
    let element = e.currentTarget;
    let id = path === 'category' ? qhCategory.getAttribute('data-cid') : qhQuestion.getAttribute('data-qid');

    postVote(base_url + '/vote/' + path + '/' + id + '/' + element.value);
}

async function postVote(url = '') {
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