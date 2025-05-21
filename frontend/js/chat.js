// chat.js — логіка для текстового та голосового чату

const chatBox = document.getElementById("chat-box");
const chatInput = document.getElementById("chat-input");
const sendButton = document.getElementById("send-button");
const voiceButton = document.getElementById("voice-button");

// Ініціалізація голосового розпізнавання
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = SpeechRecognition ? new SpeechRecognition() : null;
if (recognition) recognition.lang = "uk-UA";

function appendMessage(sender, text) {
  const msg = document.createElement("div");
  msg.className = `message ${sender}`;
  msg.innerText = text;
  chatBox.appendChild(msg);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const message = chatInput.value.trim();
  if (!message) return;

  appendMessage("user", message);
  chatInput.value = "";

  // Відправка на бекенд
  fetch("/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ message })
  })
    .then(res => res.json())
    .then(data => {
      appendMessage("bot", data.response);
    })
    .catch(err => {
      console.error("Помилка відповіді від сервера:", err);
      appendMessage("bot", "Вибач, виникла помилка.");
    });
}

sendButton.addEventListener("click", sendMessage);
chatInput.addEventListener("keypress", (e) => {
  if (e.key === "Enter") sendMessage();
});

voiceButton?.addEventListener("click", () => {
  if (!recognition) return alert("Ваш браузер не підтримує розпізнавання голосу.");

  recognition.start();

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    chatInput.value = transcript;
    sendMessage();
  };

  recognition.onerror = (event) => {
    console.error("Voice error:", event.error);
  };
});