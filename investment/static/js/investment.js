let selectedInvestment = "Mutual Funds";

function selectType(type, element) {

    selectedInvestment = type;

    document.getElementById("investmentType").value = type;

    document.querySelectorAll(".invest-card")
        .forEach(card => card.classList.remove("active"));

    element.classList.add("active");
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

    const row = document.createElement("div");

    if (sender === "user") {

        row.className = "chat-row user-row";

        row.innerHTML = `
            <div class="user-card">${message}</div>
            <div class="user-avatar">ME</div>
        `;

    } else {

        row.className = "chat-row";

        row.innerHTML = `
            <div class="bot-icon">🤖</div>
            <div class="bot-card">${message}</div>
        `;

    }

    chatBox.appendChild(row);

    chatBox.scrollTop = chatBox.scrollHeight;
}

/* TYPING INDICATOR */
function showTypingIndicator() {
    const chatBox = document.getElementById("chatBox");

    const typingDiv = document.createElement("div");
    typingDiv.classList.add("chat-bubble", "chat-bot");
    typingDiv.id = "typingIndicator";
    typingDiv.innerText = "Mitra AI is typing...";

    chatBox.appendChild(typingDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTypingIndicator() {
    const typing = document.getElementById("typingIndicator");
    if (typing) typing.remove();
}

/* SEND MESSAGE */
function sendChatMessage() {

    const input = document.getElementById("chatInput");
    const message = input.value.trim();

    if (!message) return;

    addMessageToChat(message, "user");
    input.value = "";

    showTypingIndicator();

    fetch("/investment/mitra-ai/", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: `message=${encodeURIComponent(message)}`
    })
    .then(response => response.json())
    .then(data => {
        removeTypingIndicator();
        addMessageToChat(data.reply, "bot");
    })
    .catch(error => {
        removeTypingIndicator();
        addMessageToChat("AI request failed.", "bot");
        console.error(error);
    });
}

/* ENTER KEY SUPPORT */
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

function toggleMitraChat() {
    if (window.innerWidth <= 768) {
        document.querySelector(".right-section")
                .classList.add("show-chat");
        document.body.classList.add("showing-chat");
    }
}

function closeMitraChat() {
    document.querySelector(".right-section")
            .classList.remove("show-chat");
    document.body.classList.remove("showing-chat");
}


function open_menu(){
    const menu = document.getElementById("menu");

    if(menu){
        menu.classList.toggle("show-menu");
    }
}

function setInvestment(amount, element) {

    document.getElementById("investmentAmount").value = amount;

    // remove active from all suggestion cards
    document.querySelectorAll(".suggest-btn")
        .forEach(btn => btn.classList.remove("active"));

    // activate clicked card
    element.classList.add("active");
}