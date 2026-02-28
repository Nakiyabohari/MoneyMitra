let selectedInvestment = "Mutual Funds";

function selectType(type, element) {
    selectedInvestment = type;
    document.getElementById("investmentType").value = type;

    document.querySelectorAll(".invest-card")
        .forEach(card => card.classList.remove("active"));

    element.classList.add("active");
}

/* SIDEBAR TOGGLE */
function toggleMitraChat() {
    const chat = document.getElementById("mitraChatWrapper");

    chat.classList.toggle("active");
    document.body.classList.toggle("chat-open");

    setTimeout(() => {
        const input = document.getElementById("chatInput");
        if (chat.classList.contains("active")) {
            input.focus();
        }
    }, 300);
}

/* CSRF */
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

/* ADD MESSAGE */
function addMessageToChat(message, sender) {
    const chatBox = document.getElementById("chatBox");
    const bubble = document.createElement("div");

    bubble.classList.add("chat-bubble");

    if (sender === "user") {
        bubble.classList.add("chat-user");
    } else {
        bubble.classList.add("chat-bot");
    }

    bubble.innerText = message;

    chatBox.appendChild(bubble);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* SEND MESSAGE */
function showTypingIndicator() {
    const chatBox = document.getElementById("chatBox");

    const typingDiv = document.createElement("div");
    typingDiv.classList.add("typing-bubble");
    typingDiv.id = "typingIndicator";

    typingDiv.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;

    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

function sendChatMessage() {

    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if (!message) return;

    addMessageToChat(message, "user");
    input.value = "";

    showTypingIndicator();

    const startTime = Date.now();

    fetch("/investment/mitra-ai/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: `amount=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {

        const elapsed = Date.now() - startTime;
        const minDelay = 2000; // 2 seconds minimum

        const remainingTime = minDelay - elapsed;

        setTimeout(() => {
            removeTypingIndicator();
            addMessageToChat(data.reply, "bot");
        }, remainingTime > 0 ? remainingTime : 0);

    })
    .catch(error => {
        removeTypingIndicator();
        addMessageToChat("AI request failed.", "bot");
        console.error(error);
    });
}
/* ENTER KEY */
document.addEventListener("DOMContentLoaded", function() {
    const input = document.getElementById("chatInput");

    if (input) {
        input.addEventListener("keydown", function(e) {
            if (e.key === "Enter") {
                e.preventDefault();
                sendChatMessage();
            }
        });
    }
});