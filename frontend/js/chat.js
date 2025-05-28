window.addEventListener("DOMContentLoaded", async () => {
  // const userString = localStorage.getItem("user");
  // const userId = localStorage.getItem("userId");
  const user = JSON.parse(localStorage.getItem("user"));
  const userId = user?._id?.$oid || user?._id || null;

  function updateVideoByEmotion(emotion) {
    const videoMap = {
      "😊": "happy.mp4",
      "😄": "speak_blink.mp4",
      "😲": "surprize1.mp4",
      "🤔": "squinted1.mp4",
      "😍": "surprize1.mp4"
    };
  
    const filename = videoMap[emotion] || "happy.mp4"; // fallback
    const videoElement = document.getElementById("emotion-video");
    const sourceElement = videoElement.querySelector("source");
  
    // Зміна джерела відео
    sourceElement.src = `/avatar/animations/${filename}`;
    videoElement.load(); // Завантажити нове відео
    videoElement.play(); // Запустити
  }

  if (!user) {
    alert("Користувач не авторизований");
    window.location.href = "/auth";
    return;
  }
  console.log("user:", user);
  console.log("userId:", userId);

  let sessionId = localStorage.getItem("sessionId");
  let sessionObj = localStorage.getItem("sessionId");

  try {
    if (!sessionId) {
      if (!user || !userId) {
        alert("Некоректні дані користувача");
        return;
      }
  
      const sessionResponse = await fetch(
        "http://localhost:8000/api/sessions",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            userId: userId,
            name: "Чат з FAQ",
            messages: [],
            createdAt: new Date().toISOString(),
            updatedAt: new Date().toISOString(),
          }),
        }
      );
  
      if (!sessionResponse.ok) {
        throw new Error(`Не вдалося створити сесію: ${sessionResponse.status}`);
      }
  
      
      sessionId = (await sessionResponse.text()).replace(/^"|"$/g, '');  // <-- OK
      console.log(sessionId);
      localStorage.setItem("sessionId", sessionId);
      const sessionObj = localStorage.getItem("sessionId");

      console.log("Сесія створена:", sessionObj);
    } else {
      sessionId = sessionId.replace(/^"|"$/g, '');
      console.log(sessionId);
      localStorage.setItem("sessionId", sessionId);
      console.log("Існуюча сесія:", sessionObj);
    }
  
    const sessionIdToFetch = sessionId || localStorage.getItem("sessionId");


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
      msgDiv.textContent = msg.text;  // ✅ виправлено
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
          message: message,
          sessionId: sessionObj,
          userId: userId
        }),
        
      });
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      const data = await response.json();
      updateVideoByEmotion(data.emotion);
      console.log("data.response:", data.response);
      const assistantEl = document.getElementById("assistant-text");
      console.log("assistant-text:", assistantEl);

      // Додаємо відповідь асистента зліва
      document.getElementById("assistant-text").innerText = data.response;

      // Додаємо відповідь асистента
      const assistantMsg = document.createElement("div");
      assistantMsg.className = "chat-message assistant";
      assistantMsg.textContent = data.response || "Асистент не надав відповіді.";
      console.log(data.response)
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
