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

// Function to parse DVD poster image from fsmirror pages
function readTabContent(tabInfo, callback) {
  if (!tabInfo) {
    console.warn('No tabInfo provided');
    callback("");
    return;
  }
  console.log('Attempting to parse content from tabInfo:', tabInfo.id, tabInfo.url);

  // Check if the URL contains "fsmirror" or "netflix"
  if (!tabInfo.url || (!tabInfo.url.includes('fsmirror') && !tabInfo.url.includes('netflix'))) {
    console.warn('URL does not contain "fsmirror" or "netflix":', tabInfo.url);
    callback("This function only works on fsmirror or netflix URLs");
    return;
  }

  // Check if the tab URL is valid for content script injection
  if (tabInfo.url.startsWith('chrome://') || tabInfo.url.startsWith('chrome-extension://') || 
      tabInfo.url.startsWith('edge://') || tabInfo.url.startsWith('about:')) {
    console.warn('Cannot inject script into system page:', tabInfo.url);
    callback("Cannot read content from system pages");
    return;
  }

  chrome.scripting.executeScript({
    target: {tabId: tabInfo.id},
    func: () => {
      // If Netflix, just return the URL and signal to call the wrapper
      if (window.location.href.includes('netflix')) {
        return {
          success: true,
          netflix: true,
          url: window.location.href
        };
      }
      // Parse the specific DVD poster image from the dvd-container (FSMirror)
      try {
        // Find the div with class "dvd-container" and onclick="showDvdPoster()"
        const dvdContainer = document.querySelector('div.dvd-container[onclick="showDvdPoster()"]');
        if (!dvdContainer) {
          return {
            success: false,
            error: 'DVD container not found',
            url: window.location.href,
            title: document.title || 'No title'
          };
        }
        // Find the img tag inside the dvd-container
        const imgTag = dvdContainer.querySelector('img');
        if (!imgTag || !imgTag.src) {
          return {
            success: false,
            error: 'Image tag or src attribute not found in DVD container',
            url: window.location.href,
            title: document.title || 'No title'
          };
        }
        return {
          success: true,
          imageSrc: imgTag.src,
          url: window.location.href,
          title: document.title || 'No title',
          altText: imgTag.alt || 'No alt text'
        };
      } catch (e) {
        return {
          success: false,
          error: 'Error parsing DVD poster: ' + e.message,
          url: window.location.href,
          title: document.title || 'No title'
        };
      }
    }
  }, (results) => {
    if (chrome.runtime.lastError) {
      console.error('Script injection error:', chrome.runtime.lastError.message);
      callback(`Error reading content: ${chrome.runtime.lastError.message}`);
      return;
    }
    if (!results || !results[0]) {
      console.error('No results returned from script execution');
      callback("No results returned from content script");
      return;
    }
    const result = results[0].result;
    console.log('DVD poster parsing result:', result);
    if (result.success && result.netflix) {
      // Call the wrapper directly with -n and the url
      chrome.runtime.sendNativeMessage(
        "com.example.browsertocalc",
        { netflix: true, url: result.url },
        (response) => {
          if (chrome.runtime.lastError) {
            console.error("Native Messaging Error (Netflix):", chrome.runtime.lastError.message);
          } else {
            console.log("Netflix native message sent, response:", response);
          }
        }
      );
      callback("Netflix page handled by native host");
      return;
    }
    if (result.success) {
      // Return only the img src and alt values
      const content = `${result.imageSrc}\n${result.altText}`;
      callback(content);
    } else {
      callback(`Error: ${result.error}`);
    }
  });
}

chrome.contextMenus.onClicked.addListener((info, tab) => {
  console.log('Context menu clicked:', info.menuItemId, info, tab);
  if (info.menuItemId === "sendToCalc") {
    chrome.tabs.get(tab.id, (tabInfo) => {
      console.log('sendToCalc triggered');
      // Check if this is an FSMirror page - if so, parse DVD poster info
      if (tabInfo.url && tabInfo.url.includes('fsmirror')) {
        console.log('FSMirror page detected, parsing DVD poster info');
        readTabContent(tabInfo, (content) => {
          console.log('Parsed DVD poster content:', content);
          // Extract both img src (first line) and alt text (second line) from the parsed content
          const lines = content.split('\n');
          const imageSrc = lines.length > 0 ? lines[0] : '';
          const altText = lines.length > 1 ? lines[1] : content;
          console.log('Sending alt text to Calc:', altText);
          console.log('Sending image src to Calc:', imageSrc);
          // Send alt text and image src to Calc instead of selected text
          sendToNativeHost(altText, tabInfo.url || "", imageSrc);
        });
      } else {
        // Regular functionality for non-FSMirror pages
        sendToNativeHost(info.selectionText, tabInfo.url || "");
      }
    });
  } else {
    console.warn('Unknown context menu item clicked:', info.menuItemId);
  }
});