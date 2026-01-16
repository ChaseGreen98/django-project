const chatLog = document.getElementById("chat-log");
const input = document.getElementById("chat-message-input");
const submit = document.getElementById("chat-message-submit");

const conversationId = chatLog.dataset.conversationId;
const username = chatLog.dataset.username;

if (!conversationId) {
    console.error("Conversation ID not set!");
} else {
    const socket = new WebSocket(
        "ws://" + window.location.host + "/ws/chat/" + conversationId + "/"
    );

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        chatLog.value += data.username + ": " + data.message + "\n";
        chatLog.scrollTop = chatLog.scrollHeight; // auto-scroll
    };

    submit.onclick = function() {
        const message = input.value.trim();
        if (message.length === 0) return;

        socket.send(JSON.stringify({
            "message": message,
            "username": username
        }));

        input.value = "";
    };

    input.addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            e.preventDefault();
            submit.click();
        }
    });
}

socket.onopen = () => console.log("WebSocket connected!");
socket.onerror = (err) => console.error("WebSocket error", err);