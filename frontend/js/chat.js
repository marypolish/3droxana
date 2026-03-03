window.addEventListener("DOMContentLoaded", async () => {
    const API_BASE_URL = "http://localhost:8000/api";
    
    // Елементи DOM
    const sidebar = document.getElementById("sidebar");
    const mainContent = document.getElementById("main-content");
    const toggleBtn = document.getElementById("sidebar-toggle");
    const messagesContainer = document.getElementById("messages");
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const avatarVideo = document.getElementById("avatar-video");
    const emotionLabel = document.getElementById("emotion-status");
    const newChatBtn = document.getElementById("new-chat-btn");
    const avatarBox = document.querySelector('.avatar-fixed'); // Блок для підсвітки

    const user = JSON.parse(localStorage.getItem("user"));
    const userId = user?._id?.$oid || user?._id || null;

    if (!user) {
        window.location.href = "/auth";
        return;
    }

    // Тогл меню (Sidebar)
    toggleBtn?.addEventListener("click", () => {
        sidebar.classList.toggle("collapsed");
        mainContent.classList.toggle("expanded");
    });

    // Функція виводу повідомлення
    function appendMessage(role, text) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `message ${role === "user" ? "user" : "bot"}`;
        msgDiv.textContent = text;
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // ІНІЦІАЛІЗАЦІЯ СЕСІЇ (Завантаження історії)
    async function initSession() {
        let sessionId = localStorage.getItem("sessionId");

        if (!sessionId || sessionId === "null" || sessionId === "undefined") {
            try {
                const res = await fetch(`${API_BASE_URL}/sessions`, {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({
                        userId: userId,
                        name: "Новий чат",
                        messages: [],
                        createdAt: new Date().toISOString(),
                        updatedAt: new Date().toISOString()
                    }),
                });
                if (res.ok) {
                    const rawId = await res.text();
                    sessionId = rawId.replace(/^"|"$/g, '');
                    localStorage.setItem("sessionId", sessionId);
                }
            } catch (e) { console.error("Помилка створення початкової сесії", e); }
        }

        // Завантажуємо повідомлення
        try {
            const msgRes = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);
            if (msgRes.ok) {
                const sessionData = await msgRes.json();
                messagesContainer.innerHTML = ''; 
                
                if (sessionData.messages && sessionData.messages.length > 0) {
                    sessionData.messages.forEach(msg => appendMessage(msg.role === "user" ? "user" : "bot", msg.text));
                } else {
                    appendMessage("bot", `Привіт, ${user.username || 'студенте'}! Чим можу допомогти? 👋`);
                }
            }
        } catch (e) { 
            console.error("Помилка завантаження повідомлень", e);
            appendMessage("bot", "Помилка зв'язку з сервером."); 
        }
    }

    // ВІДПРАВКА ПОВІДОМЛЕННЯ
    async function sendMessage() {
        const text = userInput.value.trim();
        const sessionId = localStorage.getItem("sessionId");
        if (!text || !sessionId) return;

        appendMessage("user", text);
        userInput.value = "";
        
        try {
            const res = await fetch(`${API_BASE_URL}/faq/chat`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: text, sessionId, userId }),
            });
            const data = await res.json();
            
            appendMessage("bot", data.response);

            // ПІДСВІТКА АВАТАРА
            if (avatarBox) {
                avatarBox.classList.add('active-glow');
                setTimeout(() => avatarBox.classList.remove('active-glow'), 3000);
            }

            // Оновлення емоції
            if (data.emotion && avatarVideo) {
                const videoMap = {
                    "neutral": "speak_blink.mp4", "happy": "happy.mp4", "sad": "sad.mp4",
                    "surprise": "surprize1.mp4", "thinking": "squinted1.mp4",
                    "😊": "happy.mp4", "😄": "speak_blink.mp4", "😲": "surprize1.mp4", "🤔": "squinted1.mp4"
                };
                const filename = videoMap[data.emotion] || "speak_blink.mp4";
                const sourceElement = avatarVideo.querySelector("source");
                if (sourceElement && !sourceElement.src.includes(filename)) {
                    sourceElement.src = `/avatar/animations/${filename}`;
                    avatarVideo.load();
                    avatarVideo.play().catch(e => console.log("Помилка відео:", e));
                    if(emotionLabel) emotionLabel.textContent = data.emotion;
                }
            }
        } catch (e) { 
            console.error("Помилка відправки", e);
            appendMessage("bot", "Помилка відправки."); 
        }
    }

    // Події кнопок
    sendBtn?.addEventListener("click", sendMessage);
    userInput?.addEventListener("keypress", (e) => { 
        if (e.key === "Enter") {
            e.preventDefault();
            sendMessage();
        }
    });

    // === НОВИЙ ЧАТ (РЕАЛІЗАЦІЯ ЧЕРЕЗ newSession) ===
    newChatBtn?.addEventListener("click", async (e) => {
        e.preventDefault();
        try {
            // Звертаємось до твого спеціального ендпоінту
            const res = await fetch(`${API_BASE_URL}/sessions/newSession`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    userId: userId,
                    name: "new Чат з FAQ",
                    messages: [],
                    createdAt: new Date().toISOString(),
                    updatedAt: new Date().toISOString()
                }),
            });
            
            if (res.ok) {
                const rawId = await res.text();
                const newSessionId = rawId.replace(/^"|"$/g, '');
                
                // Оновлюємо ID в локальному сховищі
                localStorage.setItem("sessionId", newSessionId);
                
                // Очищаємо екран і завантажуємо "чисту" сесію
                messagesContainer.innerHTML = '';
                await initSession(); 
                console.log("Нову сесію створено успішно:", newSessionId);
            } else {
                console.error("Сервер не зміг створити нову сесію");
            }
        } catch (e) { 
            console.error("Помилка при створенні нового чату:", e); 
        }
    });

    // Запуск при завантаженні
    initSession();
});