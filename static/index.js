let audio = document.querySelector("audio");

audio.addEventListener("timeupdate", () => {
    let transcription = document.getElementById("transcription").children;
    currentT = audio.currentTime;
    for (let i = 0; i < transcription.length; i++) {
        curr = transcription[i];
        if (curr.dataset.start < currentT && curr.dataset.end > currentT){
            curr.style.fontWeight = 'bold';
        } else {
            curr.style.fontWeight = 'normal';
        }
    };
});

document.addEventListener('mouseup', function(){
    let selection = window.getSelection();
    let selectedText = selection.toString().trim();    
    if (selectedText.length > 0){
        let learningSimplified = document.getElementById("learningsimplified");
        let learningPinyin = document.getElementById("learningpinyin");
        let learningTranslation = document.getElementById("learningtranslation");

        fetch("/api/dict/" + selectedText)
        .then(response => response.json())
        .then(data => {
            for (let i = 0; i < data.length; i++){
                simplified = data[i]['simplified'];
                pinyin = data[i]['pinyin'];
                english = data[i]['english'];

                if (english != null){
                    learningSimplified.textContent = simplified;
                    learningPinyin.textContent = pinyin;
                    const item = document.createElement("li");
                    const text = document.createTextNode(english);
                    item.appendChild(text);
                    learningTranslation.appendChild(item);
                } else {
                    learningSimplified.textContent = data;
                    console.log('no data found')
                    break
                }
            };
        })
    }
})

function getDefinition(clicked_id) {
    other = document.getElementById(clicked_id);
    console.log(other);

}

fetch("/api/dict/清华大学")
.then(response => response.json())
.then(data => {
    for (let i = 0; i < data.length; i++){
        console.log(data[i]['english']);
    };
})