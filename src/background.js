// Native messaging host name
const HOST_NAME = "open_in_mpv";

// Connect to native messaging host
let port = null;

function connectNativeHost() {
    port = chrome.runtime.connectNative(HOST_NAME);
    port.onDisconnect.addListener(() => {
        console.error("Disconnected from native host");
        port = null;
    });
}

// Listen for messages from content script
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.action === 'openInMpv') {
        // Ensure we're connected to native host
        if (!port) {
            connectNativeHost();
        }
        
        // Send URL to native host to open in MPV
        port.postMessage({
            action: "open",
            url: message.url
        });
    }
});
