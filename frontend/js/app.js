import { initChat, addMessage } from './chat.js';

window.addEventListener('DOMContentLoaded', () => {
  initChat();
});

async function sendMessage(message) {
  addMessage('user', message);
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ message })
    });

    const data = await response.json();
    addMessage('bot', data.reply);
  } catch (error) {
    console.error('Помилка при надсиланні повідомлення:', error);
    addMessage('bot', 'Сталася помилка при з’єднанні з сервером.');
  }
}
