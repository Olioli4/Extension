chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: "sendToCalc",
    title: "Send to LibreOffice Calc",
    contexts: ["all"] // Show in all cases, not just selection
  });
});

// Native Messaging: send selected text and URL to native host
function sendToNativeHost(selectedText, pageUrl, imageSrc = null) {
  const messageData = { 
    text: selectedText, 
    url: pageUrl || "" 
  };
  
  // Add image source if provided
  if (imageSrc) {
    messageData.imageSrc = imageSrc;
  }
  
  chrome.runtime.sendNativeMessage(
    "com.example.browsertocalc",
    messageData,
    (response) => {
      if (chrome.runtime.lastError) {
        let errorMessage = chrome.runtime.lastError.message;
        if (errorMessage.includes("host not found")) {
          console.error("Native host not found. Please check if Python script is properly registered.");
        } else if (errorMessage.includes("Native host has exited")) {
          // This is normal when the script completes successfully
          console.log("Native host completed successfully");
        } else {
          console.error("Native Messaging Error:", errorMessage);
        }
      } else if (response && response.result === "OK") {
        console.log("Successfully saved to LibreOffice Calc");
      } else if (response && response.result === "ERROR") {
        console.error("Error saving to Calc:", response.error || "Unknown error");
      } else {
        console.warn("Unexpected response:", response);
      }
    }
  );
}

function handleNetflixTab(tabInfo) {
  // Inject content script to get Netflix page title from the tab
  chrome.scripting.executeScript({
    target: {tabId: tabInfo.id},
    func: () => {
      // Try to get the Netflix video title from the player UI
      let title = null;
      const titleElem = document.querySelector('[data-uia="video-title"]');
      if (titleElem) {
        title = titleElem.textContent;
        // Trim the title to keep only the text before "Flg"
        if (title && title.includes("Flg")) {
          title = title.split("Flg")[0].trim();
        }
      }
      // Fallback to document.title if not found
      return title || document.title || '';
    }
  }, (results) => {
    let title = '';
    if (chrome.runtime.lastError) {
      console.error('Script injection error (Netflix):', chrome.runtime.lastError.message);
    } else if (results && results[0]) {
      title = results[0].result;
    }
    chrome.runtime.sendNativeMessage(
      "com.example.browsertocalc",
      { netflix: true, url: tabInfo.url, title: title },
      (response) => {
        if (chrome.runtime.lastError) {
          console.error("Native Messaging Error (Netflix):", chrome.runtime.lastError.message);
        } else {
          console.log("Netflix native message sent, response:", response);
        }
      }
    );
  });
}

function handleFSMirrorTab(tabInfo) {
  // Send only the URL to the native host, let Python handle all parsing
  chrome.runtime.sendNativeMessage(
    "com.example.browsertocalc",
    { fsmirror: true, url: tabInfo.url },
    (response) => {
      if (chrome.runtime.lastError) {
        console.error("Native Messaging Error (FSMirror):", chrome.runtime.lastError.message);
      } else {
        console.log("FSMirror native message sent, response:", response);
      }
    }
  );
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  console.log('Context menu clicked:', info.menuItemId, info, tab);
  if (info.menuItemId === "sendToCalc") {
    chrome.tabs.get(tab.id, (tabInfo) => {
      console.log('sendToCalc triggered');
      if (tabInfo.url && tabInfo.url.includes('netflix')) {
        handleNetflixTab(tabInfo);
      } else if (tabInfo.url && tabInfo.url.includes('fsmirror')) {
        handleFSMirrorTab(tabInfo);
      } else {
        // Regular functionality for non-FSMirror/non-Netflix pages
        sendToNativeHost(info.selectionText, tabInfo.url || "");
      }
    });
  } else {
    console.warn('Unknown context menu item clicked:', info.menuItemId);
  }
});