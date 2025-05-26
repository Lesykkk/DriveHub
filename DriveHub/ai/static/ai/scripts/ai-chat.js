const chatButton = document.querySelector('.ai-chat-button');
const chatContainer = document.querySelector('.ai-chat-container');
const chatScroll = document.querySelector('.ai-chat-scroll');
const chatForm = document.getElementById("chatForm");
const userInput = document.getElementById("userInput");
const messageContainer = document.querySelector(".message-container");
const systemPrompt = chatContainer.getAttribute('data-system-prompt');

let firstClick = true;

const toggleChat = function () {
    chatButton.classList.toggle('closed');
    chatContainer.classList.toggle('opened');

    if (firstClick) {
        chatScroll.scrollTop = chatScroll.scrollHeight;
        firstClick = false;
    }
}

chatForm.addEventListener("submit", async function(event) {
    event.preventDefault();

    const userMessage = userInput.value.trim();

    if (userMessage) {
        addMessageToChat(userMessage, "user");
        chatScroll.scrollTop = chatScroll.scrollHeight;
        userInput.value = "";

        const loadings = document.querySelectorAll('.loading');
        const loading = loadings[loadings.length - 1];

        loading.classList.remove("hidden");

        const response = await fetch('/ai/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                question: userMessage,
                system_prompt: systemPrompt || null
             }),
        });

        const data = await response.json();

        loading.remove();

        if (data.answer) {
            addMessageToChat(data.answer, "assistant");
            chatScroll.scrollTop = chatScroll.scrollHeight;
        }
    }

    chatScroll.scrollTop = chatScroll.scrollHeight;
});

function addMessageToChat(messageText, sender) {
    const messageBlock = document.createElement("div");
    messageBlock.classList.add("message-block", sender);

    const iconColumn = document.createElement("div");
    iconColumn.classList.add("icon-column");

    if (sender === "assistant") {
        const messageIcon = document.createElement("img");
        const messageIconSrc = chatContainer.querySelector('.logo img').src;
        messageIcon.classList.add("message-profile-icon");
        messageIcon.src = messageIconSrc;
        iconColumn.appendChild(messageIcon);
    }

    const messageColumn = document.createElement("div");
    messageColumn.classList.add("message-column");

    const message = document.createElement("div");
    message.classList.add("message");
    message.textContent = messageText;

    const loadingDiv = document.createElement("div");
    loadingDiv.classList.add("loading");
    loadingDiv.classList.add("hidden");

    messageColumn.appendChild(message);
    messageColumn.appendChild(loadingDiv);
    messageBlock.appendChild(iconColumn);
    messageBlock.appendChild(messageColumn);
    messageContainer.appendChild(messageBlock);
}

async function loadChatHistory() {
    const response = await fetch('/ai/chat/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    });

    const data = await response.json();

    if (data.chat_history) {
        data.chat_history.forEach(message => {
            addMessageToChat(message.content, message.role);
        });

        chatScroll.scrollTop = chatScroll.scrollHeight;
    }
}

loadChatHistory();