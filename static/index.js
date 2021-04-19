function copyToClip(){
    const element = document.getElementById("new_url");
    copyToClipboard(element.placeholder);
}

function copyToClipboard(text) {
    if (window.clipboardData && window.clipboardData.setData) {
        // Internet Explorer-specific code path to prevent textarea being shown while dialog is visible.
        return window.clipboardData.setData("Text", text);

    }
    else if (document.queryCommandSupported && document.queryCommandSupported("copy")) {
        var textarea = document.createElement("textarea");
        textarea.textContent = text;
        textarea.style.position = "fixed";  // Prevent scrolling to bottom of page in Microsoft Edge.
        document.body.appendChild(textarea);
        textarea.select();
        try {
            return document.execCommand("copy");  // Security exception may be thrown by some browsers.
        }
        catch (ex) {
            window.alert("Copy to clipboard failed.");
            return false;
        }
        finally {
            document.body.removeChild(textarea);
        }
    }
}

function deleteUrl(code){
    fetch("/delete-url",{
        method: "POST",
        body: JSON.stringify({code: code})
    }).then((_res)=>{
        window.location.href="/dashboard"
    })
}