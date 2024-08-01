text_lesson_form = document.getElementById("textlessonform");
download_html_form = document.getElementById("downloadhtmlform");

document.getElementById("learninglevels").style.display = "none";

// load form options
fetch("/api/lessons/text/")
.then(response => response.json())
.then(data => {
    lessons_selector = document.getElementById("lessonselector")
    for (let i = 0; i < data.length; i++){
        const option = document.createElement("option");
        console.log(data[i])
        option.textContent = data[i].split('.')[0];
        option.dataset.filename = data[i];
        lessons_selector.appendChild(option);
    };
});
// form submission
text_lesson_form.addEventListener("submit", (e) => {
    e.preventDefault();
    transcript_div = document.getElementById("transcript");
    transcript_div.innerHTML = "";
    select_element = document.getElementById("lessonselector");
    filename = select_element.options[select_element.selectedIndex].dataset.filename; //IMPT part
    async function createHTMLElements() {
        try {
            const segwords_res = await fetch("/api/lessons/text/" + filename); //returns {'word','pos'}
            const segwords_json = await segwords_res.json();
            const batch_size = 100;
            let batches = [];
            for (let i = 0; i < segwords_json.length; i+=batch_size){
                batches.push(segwords_json.slice(i , i + batch_size))
            }
            console.log(batches);
            const levels_promises = await Promise.all(batches.map( batch => 
                fetch("/api/knowledge_level", 
                    {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                      },      
                    body: JSON.stringify({ 'batch' : batch })
                    }
                )
            ));
            const batch_levels_json = await Promise.all(levels_promises.map(r => r.json()));
            
            const levels_json = batch_levels_json.flat();
            const data = segwords_json;
            regex = /\p{P}/u; //testing for punctuation
            data.forEach((item, index) => {
                word = item['word'];
                if (word == '\n') {
                    transcript_div.appendChild(document.createElement("br"));
                } else if (word == ' ') {
                    transcript_div.appendChild(document.createTextNode(" "));
                } else if (regex.test(word)) {
                    transcript_div.appendChild(document.createTextNode(word));
                } else {
                    const level = levels_json[index];
                    const span_element = document.createElement("span");
                    span_element.classList.add('indiv');
                    span_element.classList.add(word);
                    span_element.setAttribute("onclick", "getDefinition(this)")
                    span_element.textContent = word;
                    span_element.dataset.pos = item['pos'];

                    span_element.dataset.level = level;
                    if (level <= 0){
                        span_element.style.backgroundColor = '#B2FFFF';
                    } else if ( level <= 5 ) {
                        opacity_value = (1 - level/5);
                        span_element.style.backgroundColor = `rgba(237, 233, 157, ${opacity_value})`;
                    };
                    transcript_div.appendChild(span_element); 
                };
            });
        } catch (err) {
            console.log(err);
        }
    }
    createHTMLElements(); // {word, pos, level}
});    

//getWordDefinition
function getDefinition(clicked_element) {
    const selected_word = clicked_element.textContent;
    let learningSimplified = document.getElementById("learningsimplified");
    if (selected_word == learningSimplified.textContent){
        console.log("same data selected")
    }
    else if (selected_word.length > 0){
        let learningPinyin = document.getElementById("learningpinyin");
        let learningTranslation = document.getElementById("learningtranslation");
        let learningPos = document.getElementById("learningpos");
        learningSimplified.innerHTML = '';
        learningPinyin.innerHTML = '';
        learningTranslation.innerHTML = '';
        learningPos.innerHTML = '';
        fetch("/api/dict/" + selected_word)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++){
                if (data[i]['english'] != null){
                    learningSimplified.textContent = data[i]['simplified'];
                    learningPinyin.textContent = data[i]['pinyin'];
                    learningPos.textContent = "(" + clicked_element.dataset.pos + ")";
                    const item = document.createElement("li");
                    const text = document.createTextNode(data[i]['english']);
                    item.appendChild(text);
                    learningTranslation.appendChild(item);
                } else {
                    learningSimplified.textContent = data;
                    console.log('no data found')
                    break
                }
            };
            let learningDiv = document.getElementById("learninglevels"); 
            let leveloptions = document.getElementsByClassName("leveloptions"); 
            if (learningDiv.style.display === "none"){
                learningDiv.style.display = "block";
            }; 
            for (let i=0; i <=5; i ++ ){
                leveloptions[i].style.backgroundColor = 'transparent';
            }
            leveloptions[clicked_element.dataset.level].style.backgroundColor = 'aquamarine';
        });
    }
}

function updateLevel(clicked_option) {
    const updatedlevel = clicked_option.dataset.level;
    console.log(updatedlevel);
    const word = document.getElementById("learningsimplified").textContent;
    const requestOptions = {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
          },      
        body: JSON.stringify( { 
            'word' : word,
            'level' : updatedlevel 
        })
    };
    fetch("/api/knowledge_level", requestOptions)
    .then(response => response.json())
    .then(data => {
        console.log(data);
        const all_instances = document.getElementsByClassName(word);
        for (let i = 0; i < all_instances.length; i ++){
            item = all_instances[i];
            item.dataset.level = updatedlevel;
            if (updatedlevel <= 0){
                item.style.backgroundColor = '#B2FFFF';
            } else if ( updatedlevel <= 5 ) {
                opacity_value = (1 - updatedlevel/5);
                item.style.backgroundColor = `rgba(255, 234, 0, ${opacity_value})`;
            };
        }
        let leveloptions = document.getElementsByClassName("leveloptions"); 
        for (let i=0; i <=5; i ++ ){
            leveloptions[i].style.backgroundColor = 'transparent';
        }
        leveloptions[updatedlevel].style.backgroundColor = 'aquamarine';
    });
}

//Scrape Web
download_html_form.addEventListener("submit", (e)=>{
    e.preventDefault();
    const url = document.getElementById("htmlurl").value;
    fetch('/api/parse/text/?' + new URLSearchParams({
        url: url,
    }).toString())
    .then(response => response.json())
    .then(data => {
        console.log("success")
    })
    
})

