const fetch_btn = document.getElementById("fetch-btn");

fetch_btn.addEventListener("click", () => {
    console.log("Test 1");

    chrome.tabs.query( { active: true, currentWindow: true }, (tabs) => {
        console.log("Test 2");
        chrome.scripting.executeScript({
            target: { tabId: tabs[0].id },
            files: ["content.js"]
        });
      });
      
})


// https://github.com/Tshetrim/Image-To-Text-OCR-extension-for-ChatGPT?tab=readme-ov-file
// https://github.com/naptha/tesseract.js?tab=readme-ov-file#tesseractjs


// Code that works //

// const fetch_btn = document.getElementById("fetch-btn");

// fetch_btn.addEventListener("click", () => {
//     console.log("Test 1");
//     chrome.tabs.query( { active: true, currentWindow: true }, (tabs) => {
//         console.log("Test 2");
//         chrome.scripting.executeScript({
//             target: { tabId: tabs[0].id },
//             func: getImg
//         }, (promise) => { //promise array of InjectionResult fulfilled after getImg function, has property result
//             let testdiv = document.getElementById("testdiv");
//             const results = promise[0].result;
//             for (let i = 0; i < results.length; i ++){
//                 console.log("promise" + results[i]);
//                 let pp = document.createElement("p");
//                 pp.textContent = results[i];
//                 testdiv.appendChild(pp);
//             };
//         });
//       });
      
// })

// const getImg = () => {
//     console.log("Test 3: " + document.body);
//     const imgs = document.getElementsByTagName('img');
//     const canvass = document.getElementsByTagName('canvas');
//     const img_url = [];
//     for (let i = 0; i < imgs.length; i ++){
//         if (imgs[i].hasAttribute('loading') || imgs[i].hasAttribute('lazy')){
//             console.log("has lazy")
//             img_url.push(imgs[i].dataset.src);
//         } else {
//             img_url.push(imgs[i].src);
//         };
//     }
//     for (let i = 0; i < canvass.length; i ++){
//         // let target = new Image();
//         canvass[i].toBlob((blob) => {
//             const url = URL.createObjectURL(blob);
//             img_url.push(url);
//             console.log("canvas:" + url);
//         });
//     }
//     console.log("returned text: " + text);
//     return img_url;
// }
