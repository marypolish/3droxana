window.addEventListener("DOMContentLoaded", async () => {
  // const userString = localStorage.getItem("user");
  // const userId = localStorage.getItem("userId");
  const user = JSON.parse(localStorage.getItem("user"));
  const userId = user?._id?.$oid || user?._id || null;

  if (!user) {
    alert("Користувач не авторизований");
    window.location.href = "/auth";
    return;
  }
  console.log("user:", user);
  console.log("userId:", userId);

  let sessionId = localStorage.getItem("sessionId");
  let sessionObj = sessionId ? JSON.parse(sessionId) : null;

  try {
    if (!sessionId) {
      if (!user || !userId) {
        alert("Некоректні дані користувача");
        return;
      }

      // 1. Створення сесії, якщо ще не створено
      const sessionResponse = await fetch(
        "http://localhost:8000/api/sessions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userId: userId,
            name: "Чат з FAQ", // або інша назва сесії
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          }),
        }
      );

      if (!sessionResponse.ok) {
        throw new Error(`Не вдалося створити сесію: ${sessionResponse.status}`);
      }

      sessionId = await response.text(); // бекенд повертає id сесії як рядок
      // Зберігаємо сесію у localStorage
      localStorage.setItem("sessionId", JSON.stringify({ _id: sessionId }));
      sessionObj = { _id: sessionId };
      console.log("Сесія створена:", sessionObj);
    } else {
      console.log("Існуюча сесія:", sessionObj);
    }

    // Завантажуємо повідомлення сесії по ID
    // Припускаємо, що sessionObj має _id або id, потрібно вказати правильний ідентифікатор
    const sessionIdToFetch = sessionObj._id || sessionObj.id || sessionObj;
    const messagesRes = await fetch(
      `http://localhost:8000/api/sessions/${sessionIdToFetch}`
    );
    if (!messagesRes.ok) {
      throw new Error("Не вдалося отримати повідомлення сесії");
    }
    const sessionData = await messagesRes.json();

    const chatWindow = document.querySelector(".chat-window");
    sessionData.messages.forEach((msg) => {
      const msgDiv = document.createElement("div");
      msgDiv.className =
        "chat-message " + (msg.role === "user" ? "user" : "assistant");
      msgDiv.textContent = msg.content;
      chatWindow.appendChild(msgDiv);
    });

    chatWindow.scrollTop = chatWindow.scrollHeight;
  } catch (err) {
    console.error("Помилка ініціалізації сесії:", err);
    alert("Не вдалося запустити сесію чату.");
    return;
  }

  // Обробка кнопки та клавіші Enter
  document.getElementById("send-btn").addEventListener("click", sendMessage);
  document
    .getElementById("user-input")
    .addEventListener("keypress", function (e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
      }
    });

  async function sendMessage() {
    const input = document.getElementById("user-input");
    const message = input.value.trim();
    if (!message) return;
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
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          userId: userId,
          sessionId: sessionObj._id || sessionObj.id || sessionObj,
          message,
        }),
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
      assistantMsg.textContent =
        data.response || "Асистент не надав відповіді.";
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
});
