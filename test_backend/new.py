
from openai import OpenAI


from pymongo import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://laartemser:h3G6Zdzl7C2DAiYV@3davatar.jd7ic5f.mongodb.net/?retryWrites=true&w=majority&appName=3davatar"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    db = client["3davatar"]
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)




faq_collection = db["faq"]


"""Пошук схожих питань за ключовими словами."""
def search_faq(question: str, limit=3):
    keywords = question.lower().split()
    query = {
        "visible": True,
        "$or": [
            {"question": {"$regex": kw, "$options": "i"}}
            for kw in keywords
        ]
    }
    return list(faq_collection.find(query).limit(limit))


# 🔁 Підключення до OpenRouter API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # ✅ OpenRouter endpoint
    api_key="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",  # 🔑 Встав сюди свій особистий API-ключ з https://openrouter.ai
)


while True:
    question = input("\nВаше питання (або 'вийти'): ")
    if question.lower() == 'вийти':
        break

    results = search_faq(question)

    if not results:
        print("Нічого не знайдено у базі 😢")
        continue

    # Створюємо контекст для ШІ
    context = "\n\n".join([
        f"Питання: {item['question']}\nВідповідь: {item['answer']}\nПосилання: {item['source']}"
        for item in results
    ])

    response = client.chat.completions.create(
        model="google/gemma-3-4b-it:free",
         messages=[
        {
            "role": "system",
            "content": (
                "Ти чат-асистент для студентів КПІ. "
                "Твоє завдання — проаналізувати зміст запиту користувача та знайти максимально релевантні записи з бази знань. "
                "Ти не вигадуєш інформацію самостійно — відповідай лише на основі наданого контексту. "
                "Наприкінці кожної відповіді додай посилання на джерело, якщо воно є. "
                "Також, якщо користувач не ставить питання щодо КПІ, а просто хоче поспілкуватися, ти можеш відповісти на запит, "
                "вказавши, що це твоя суб'єктивна думка і ти не спираєшся на жодне джерело."
                "Наприкінці відповідай з відповідною емоцією: 😡, 😄, 🤔, 😞 тощо, залежно від емоційного забарвлення запиту."
            )
        },
        {"role": "user", "content": f"Контекст:\n{context}"},
        {"role": "user", "content": question}
    ]
    )

    print("🤖 Відповідь:", response.choices[0].message.content)