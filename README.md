Option (1)
regex = /\p{P}/u; //testing for punctuation
for (const batch of batches) {
const res = await fetch("/api/knowledge_level",
{
method: 'POST',
headers: {
'Content-Type': 'application/json',
},
body: JSON.stringify({ 'batch' : batch })
}
)
const batch_levels_json = await res.json();
console.log(batch_levels_json);
batch.forEach((item, token_index) => {
token = item['word'];
if (token == '\n') {
transcript_div.appendChild(document.createElement("br"));
} else if (token == ' ') {
transcript_div.appendChild(document.createTextNode(" "));
} else if (regex.test(token)) {
transcript_div.appendChild(document.createTextNode(token));
} else {
const level = batch_levels_json[token_index];
const span_element = document.createElement("span");
span_element.classList.add('indiv');
span_element.classList.add(token);
span_element.setAttribute("onclick", "getDefinition(this)")
span_element.textContent = token;
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
    })

}

Option (2)
regex = /\p{P}/u; //testing for punctuation
Promise.all(batches.map(async (batch) => {
const res = await fetch("/api/knowledge_level",
{
method: 'POST',
headers: {
'Content-Type': 'application/json',
},  
 body: JSON.stringify({ 'batch' : batch })
}
)
const batch_levels_json = await res.json();
console.log(batch_levels_json);

    batch.forEach((item, token_index) => {
        token = item['word'];
        if (token == '\n') {
            transcript_div.appendChild(document.createElement("br"));
        } else if (token == ' ') {
            transcript_div.appendChild(document.createTextNode(" "));
        } else if (regex.test(token)) {
            transcript_div.appendChild(document.createTextNode(token));
        } else {
            const level = batch_levels_json[token_index];
            const span_element = document.createElement("span");
            span_element.classList.add('indiv');
            span_element.classList.add(token);
            span_element.setAttribute("onclick", "getDefinition(this)")
            span_element.textContent = token;
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
    })

}))
