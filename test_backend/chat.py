from openai import OpenAI
from scraper import get_page_info

# 🔁 Використовуємо Groq API
client = OpenAI(
    base_url="https://api.groq.com/openai/v1",
    api_key="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"  # Замінити на твій особистий ключ з https://console.groq.com/
)

# Отримання контексту зі сторінки
url = "https://iate.kpi.ua/ua/127-vikladackiy-sklad-kafedra-inzhenerii-programnogo-zabezpechennya-v-energetici"
context = get_page_info(url)

while True:
    question = input("\nВаше питання (або 'вийти'): ")
    if question.lower() == 'вийти':
        break

    response = client.chat.completions.create(
        model="mistral-saba-24b",  # 🔁 Замість gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "Ти помічник, який відповідає на основі тексту."},
            {"role": "user", "content": f"Контекст:\n{context}"},
            {"role": "user", "content": question}
        ]
    )

    print("Відповідь:", response.choices[0].message.content)
