/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

let preview = false;

function toggleLivePreview() {
    let checkbox = document.getElementById('descriptionPreviewCheckbox');
    let prev = document.getElementById('descriptionPreviewDiv');
    let prev2 = document.getElementById('descriptionPreviewP');
    if(checkbox.checked) {
        preview = true;
        prev.classList.remove('hidden');
        prev2.classList.remove('hidden');
        prev.classList.remove('invisible');
        prev2.classList.remove('invisible');
        livePreviewTrigger();
    } else {
        preview = false;
        prev.classList.add('hidden');
        prev2.classList.add('hidden');
        prev.classList.add('invisible');
        prev2.classList.add('invisible');
    }
}

function livePreviewTrigger() {
    // Change descriptionCharacterLeft amount
    let input = document.getElementById('newDescription');
    let output = document.getElementById('descriptionPreviewP');
    let charLeft = document.getElementById('descriptionCharacterLeft');
    charLeft.innerHTML = String(1000 - input.value.length) + " Zeichen verbleibend";
    let html = /(<([a-zA-Z \/!])+([^>])*)/;
    let content = input.value.replace(html, '');

    if(!preview) return;
    output.innerHTML = marked(content);
}

marked.setOptions({
   breaks: true
});

let desc = document.getElementById('newDescription');
let charLeft = document.getElementById('descriptionCharacterLeft');
charLeft.innerHTML = String(1000 - desc.value.length) + " Zeichen verbleibend";