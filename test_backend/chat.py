from openai import OpenAI
from scraper import get_page_info

# 🔁 Підключення до OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # ✅ OpenRouter endpoint
    api_key="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",  # 🔑 Встав сюди свій особистий API-ключ з https://openrouter.ai
)

# Отримання контексту зі сторінки
url = "https://iate.kpi.ua/ua/127-vikladackiy-sklad-kafedra-inzhenerii-programnogo-zabezpechennya-v-energetici"
context = get_page_info(url)

while True:
    question = input("\nВаше питання (або 'вийти'): ")
    if question.lower() == 'вийти':
        break

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",  # ✅ Рекомендована безкоштовна модель
        messages=[
            {"role": "system", "content": "Ти помічник, який відповідає на основі тексту."},
            {"role": "user", "content": f"Контекст:\n{context}"},
            {"role": "user", "content": question}
        ]
    )

    print("Відповідь:", response.choices[0].message.content)
