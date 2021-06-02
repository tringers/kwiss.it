/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */

const format = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;

function validatePassword(element, errorField) {
    let value = element.value;
    if (errorField !== null)
        errorField.innerHTML = '';

    if (value.length < 8 && errorField !== null) {
        errorField.innerHTML = 'Passwort zu kurz!';
    }

    if (value.length > 64 && errorField !== null) {
        errorField.innerHTML = 'Passwort zu lang!';
    }

    let strength = 0;
    let uc = false;
    let lc = false;
    let di = false;
    let sc = false;

    for (let i = 0; i < value.length; i++) {
        let char = value.charAt(i);
        if (char >= '0' && char <= '9') {
            if (di) continue;
            di = true;
            strength += 1;

        } else if (format.test(char)) {
            if (sc) continue;
            sc = true;
            strength += 1;
        } else if (char === char.toLowerCase()) {
            if (lc) continue;
            lc = true;
            strength += 1;
        } else if (char === char.toUpperCase()) {
            if (uc) continue;
            uc = true;
            strength += 1;
        }
    }

    if (strength < 3 && errorField !== null) {
        errorField.innerHTML = 'Passwort entspricht nicht den Voraussetzungen!';
    }
}

function testUsername() {
    let input = document.getElementById('regInputUsername').value;
    let status = document.getElementById('usernameStatus');
    fetch('/register/checkusername/' + encodeURI(input))
        .then(res => res.json()
            .then(data => {
                if(parseInt(data.status) !== 200) {
                    status.innerHTML = data.message;
                } else {
                    status.innerHTML = '';
                }
            })
        );
}

// Add Listener
document.getElementById('regInputUsername').addEventListener('focusout', testUsername);

let ePW = document.getElementsByClassName('validate-password');
let ePWE = document.getElementsByClassName('validate-password-error');
for (let i = 0; i < ePW.length; i++) {
    let e = ePW[i];
    e.addEventListener('input', () => {
        validatePassword(e, ePWE.length >= i ? ePWE[i] : null);
    })
}

let elPassIdentFirst = document.getElementsByClassName('validate-password-identical-first');
let elPassIdentSecond = document.getElementsByClassName('validate-password-identical-second');
let elPassIdentErr = document.getElementsByClassName('validate-password-identical-error');
let ePWIF = null, ePWIS = null, ePWIE = null;

if (elPassIdentFirst.length >= 1)
    ePWIF = elPassIdentFirst[0];

if (elPassIdentSecond.length >= 1)
    ePWIS = elPassIdentSecond[0];

if (elPassIdentErr.length >= 1)
    ePWIE = elPassIdentErr[0];

if (ePWIF !== null && ePWIS !== null && ePWIE !== null) {
    ePWIS.addEventListener('input', () => {
        if (ePWIS.value !== ePWIF.value) {
            ePWIE.innerHTML = 'Passwörter sind nicht identisch!';
        } else {
            ePWIE.innerHTML = '';
        }
    });
}