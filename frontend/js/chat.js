// Обробка натискання кнопки "Надіслати"
document.getElementById("send-btn").addEventListener("click", sendMessage);

// Обробка Enter у полі введення
document.getElementById("user-input").addEventListener("keypress", function (e) {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault(); // Щоб не вставлявся новий рядок
    console.log("sendMessage")
    sendMessage();
  }
});

async function sendMessage() {
  const input = document.getElementById("user-input");
  const message = input.value.trim();
  if (message === "") return;
  console.log("sendMessage")
  const chatWindow = document.querySelector(".chat-window");

  // Додаємо повідомлення користувача
  const userMsg = document.createElement("div");
  userMsg.className = "chat-message user";
  userMsg.textContent = message;
  chatWindow.appendChild(userMsg);

  input.value = "";

  // Прокручуємо вниз чат
  chatWindow.scrollTop = chatWindow.scrollHeight;

  // Відправка запиту до бекенду
  try {
    const response = await fetch("http://localhost:8000/api/faq/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    console.log("data.response:", data.response);
    const assistantEl = document.getElementById("assistant-text");
    console.log("assistant-text:", assistantEl);

    // Додаємо відповідь асистента зліва
    document.getElementById("assistant-text").innerText = data.response;

    // Додаємо відповідь асистента
    const assistantMsg = document.createElement("div");
    assistantMsg.className = "chat-message assistant";
    assistantMsg.textContent = data.response || "Асистент не надав відповіді.";
    chatWindow.appendChild(assistantMsg);
    

    chatWindow.scrollTop = chatWindow.scrollHeight;
  } catch (err) {
    console.error("Помилка відповіді від сервера:", err);
    const errorMsg = document.createElement("div");
    errorMsg.className = "chat-message assistant";
    errorMsg.textContent = "Вибач, виникла помилка при зверненні до сервера.";
    chatWindow.appendChild(errorMsg);
  }
}

