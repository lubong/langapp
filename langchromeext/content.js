console.log("content script test 1");
const imgs = document.getElementsByTagName('img');
const canvass = document.getElementsByTagName('canvas');

//print all the URLs
// for (let i = 0; i < imgs.length ; i ++){
//     console.log("image URL : " + imgs[i].src);
// }

chrome.runtime.sendMessage({
    greeting: "Greeting from the content script",
  }).then( (res) => {
    console.log('message from background script' + res.response);
  }, (error) => {
    console.log("error: " + error);
  });


// (async () => {
//     console.log("async is starting");
//     const worker = await Tesseract.createWorker("eng");
//     for (let i = 0; i < imgs.length ; i ++){
//         try {
//             const { data: { text } } = await worker.recognize(imgs[i]);
//             console.log("worker success: " + text);
//         }
//         catch(error) {
//             console.log("error");
//         }
//     }
//     console.log("success text")
//     await worker.terminate();
// })();






// (async () => {
//     console.log("async is starting");
//     const worker = await Tesseract.createWorker("eng");
//     for (let i = 0; i < imgs.length ; i ++){
//         try {
//             const { data: { text } } = await worker.recognize(imgs[i]);
//             console.log("worker success: " + text);
//         }
//         catch(error) {
//             console.log("error");
//         }
//     }
//     console.log("success text")
//     await worker.terminate();
// })();
