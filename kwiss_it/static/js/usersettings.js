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
        prev.hidden = false;
        livePreviewTrigger();
    } else {
        preview = false;
        prev.hidden = true;
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

// Add Listener
document.getElementById('descriptionPreviewCheckbox').addEventListener('click', toggleLivePreview);
document.getElementById('newDescription').addEventListener('input', livePreviewTrigger);

marked.setOptions({
   breaks: true
});

let desc = document.getElementById('newDescription');
let charLeft = document.getElementById('descriptionCharacterLeft');
charLeft.innerHTML = String(1000 - desc.value.length) + " Zeichen verbleibend";