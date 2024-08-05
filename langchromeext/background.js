console.log("background 1");

chrome.runtime.onMessage.addListener( (request, sender, sendResponse) => {
    console.log(`A content script sent a message: ${request.greeting}`);
    sendResponse({ response: "Response from background script" });
});