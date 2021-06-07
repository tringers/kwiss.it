/*
IMPORTANT:
After changing code in here:
  Please run jsmin.bat or equivalent.
 */
let cattemplate="templateaccordionitemclass";
let qtemplate="templateaccordionitemquestion";
let atemplate="templateanswer";

function start(){

}
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



document.addEventListener("DOMContentLoaded", start);
