$(document).ready(function () {
 
    var subtitleInterval = null;
 
    function showSubtitle(msg) {
        var el = document.getElementById("jarvis-subtitle-text");
        if (!el) return;
        if (subtitleInterval) { clearInterval(subtitleInterval); subtitleInterval = null; }
        el.textContent = "";
        var words = msg.split(" "), i = 0;
        subtitleInterval = setInterval(function () {
            if (i < words.length) { el.textContent += (i === 0 ? "" : " ") + words[i++]; }
            else { clearInterval(subtitleInterval); subtitleInterval = null; }
        }, 120);
    }
 
    function clearSubtitle() {
        var el = document.getElementById("jarvis-subtitle-text");
        if (el) el.textContent = "";
        if (subtitleInterval) { clearInterval(subtitleInterval); subtitleInterval = null; }
    }
 
    function jAvatar() {
        return '<div class="j-avatar">' +
            '<div class="ring1"></div>' +
            '<div class="ring2"></div>' +
            '<div class="ring3"></div>' +
            '<div class="jcenter"><div class="jdot"></div></div>' +
        '</div>';
    }
 
    function addJarvisMessage(message) {
        if (!message || !message.trim()) return;
        var chatBody = document.getElementById("main-chat-body");
        if (!chatBody) return;
        var ph = document.getElementById("chat-placeholder");
        if (ph) ph.remove();
 
        var row = document.createElement("div");
        row.style.cssText = "display:flex;align-items:flex-end;gap:10px;";
        row.innerHTML = jAvatar() +
            '<div class="j-bubble typing-bubble"></div>';
        chatBody.appendChild(row);
        chatBody.scrollTop = chatBody.scrollHeight;
 
        var bubble = row.querySelector(".typing-bubble");
        var words = message.split(" "), idx = 0;
        var t = setInterval(function () {
            if (idx < words.length) {
                bubble.textContent += (idx === 0 ? "" : " ") + words[idx++];
                chatBody.scrollTop = chatBody.scrollHeight;
            } else { clearInterval(t); }
        }, 80);
    }
 
    function addUserMessage(message) {
        if (!message || !message.trim()) return;
        var chatBody = document.getElementById("main-chat-body");
        if (!chatBody) return;
        var ph = document.getElementById("chat-placeholder");
        if (ph) ph.remove();
 
        var row = document.createElement("div");
        row.style.cssText = "display:flex;justify-content:flex-end;";
        row.innerHTML = '<div class="u-bubble">' + message + '</div>';
        chatBody.appendChild(row);
        chatBody.scrollTop = chatBody.scrollHeight;
    }
 
    // ===== EEL EXPOSED =====
 
    eel.expose(DisplayMessage)
    function DisplayMessage(message) {
        showSubtitle(message);
        $(".siri-message .texts li").text(message);
        try { $('.siri-message').textillate('start'); } catch(e) {}
    }
 
    eel.expose(ShowHood)
    function ShowHood() {
        $("#Oval").attr("hidden", false);
        $("#SiriWave").attr("hidden", true);
        clearSubtitle();
    }
 
    eel.expose(senderText)
    function senderText(message) {
        if (!message || !message.trim()) return;
        addUserMessage(message);
        var cb = document.getElementById("chat-canvas-body");
        if (cb) {
            cb.innerHTML += '<div class="row justify-content-end mb-4"><div class="width-size"><div class="sender_message">' + message + '</div></div></div>';
            cb.scrollTop = cb.scrollHeight;
        }
    }
 
    eel.expose(receiverText)
    function receiverText(message) {
        if (!message || !message.trim()) return;
        addJarvisMessage(message);
        var cb = document.getElementById("chat-canvas-body");
        if (cb) {
            cb.innerHTML += '<div class="row justify-content-start mb-4"><div class="width-size"><div class="receiver_message">' + message + '</div></div></div>';
            cb.scrollTop = cb.scrollHeight;
        }
    }
 
    eel.expose(hideLoader)
    function hideLoader() {
        $("#Loader").attr("hidden", true);
        $("#FaceAuth").attr("hidden", false);
    }
 
    eel.expose(hideFaceAuth)
    function hideFaceAuth() {
        $("#FaceAuth").attr("hidden", true);
        $("#FaceAuthSuccess").attr("hidden", false);
    }
 
    eel.expose(hideFaceAuthSuccess)
    function hideFaceAuthSuccess() {
        $("#FaceAuthSuccess").attr("hidden", true);
        $("#HelloGreet").attr("hidden", false);
    }
 
    eel.expose(hideStart)
    function hideStart() {
        $("#Start").attr("hidden", true);
        setTimeout(function () {
            $("#Oval").addClass("animate__animated animate__zoomIn");
            $("#Oval").attr("hidden", false);
        }, 1000);
    }
 
});