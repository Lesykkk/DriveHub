const chatButton = document.querySelector('.ai-chat-button');
const chatContainer = document.querySelector('.ai-chat-container');
const chatScroll = document.querySelector('.ai-chat-scroll');

let fistClick = true;

const toggleChat = function () {
    chatButton.classList.toggle('closed');
    chatContainer.classList.toggle('opened');

    if (fistClick) {
        chatScroll.scrollTop = chatScroll.scrollHeight;
        fistClick = false;
    }
}