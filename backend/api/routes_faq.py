from fastapi import APIRouter, Depends, HTTPException
from ..db.mongodb import get_database
from ..models import faq as faq_model
from ..schemas import faq as faq_schema
from pydantic import BaseModel
from openai import OpenAI
import asyncio
import traceback
from httpx import Client
import re
from bson import ObjectId
from datetime import datetime
from together import Together
router = APIRouter(prefix="/api/faq", tags=["FAQ"])


client = Together(api_key="137f302b0bb50bb26cbf1f491b2bf183bf54c1bebd7df461ac9d0441f8f7f9d7")
# client = OpenAI(
#     base_url="https://openrouter.ai/api/v1",  # ✅ OpenRouter endpoint
#     api_key="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",  
#     http_client=Client(trust_env=False)# 🔑 Встав сюди свій особистий API-ключ з https://openrouter.ai
# )

@router.get("/", response_model=list[faq_schema.FAQOut])
async def read_all_faqs(db=Depends(get_database)):
    return await faq_model.get_all_faqs(db)

@router.get("/{id}", response_model=faq_schema.FAQOut)
async def read_faq(id: str, db=Depends(get_database)):
    faq = await faq_model.get_faq_by_id(db, id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq

@router.post("/", response_model=str)
async def create_faq(faq: faq_schema.FAQCreate, db=Depends(get_database)):
    return await faq_model.create_faq(db, faq.dict())

@router.put("/{id}")
async def update_faq(id: str, faq: faq_schema.FAQUpdate, db=Depends(get_database)):
    await faq_model.update_faq(db, id, faq.dict())
    return {"message": "FAQ updated successfully"}

@router.delete("/{id}")
async def delete_faq(id: str, db=Depends(get_database)):
    await faq_model.delete_faq(db, id)
    return {"message": "FAQ deleted successfully"}

class ChatRequest(BaseModel):
    message: str
    sessionId: str
    userId: str

class ChatResponse(BaseModel):
    response: str
    link: str
    emotion: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_faq(request: ChatRequest, db=Depends(get_database)):
    message = request.message.strip()
    session_id = request.sessionId
    print("📥 Отримано запит:", request.dict())
    # Пошук FAQ релевантних
    # faqs = await faq_model.get_all_faqs(db)
    # relevant = []
    # for faq in faqs:
    #     if message in faq["question"].lower() or message in faq["answer"].lower():
    #         relevant.append(faq)
    #         if len(relevant) >= 3:  # максимум 3 для контексту
    #             break

    # # Формуємо контекст
    # context = "\n\n".join([
    #     f"Питання: {item['question']}\nВідповідь: {item['answer']}\nДжерело: {item.get('source', 'немає')}"
    #     for item in relevant
    # ])
    links = await db["links"].find().to_list(None)
    context = "\n\n".join([
        f"{i+1}) Назва: {link['title']}\nОпис: {link['description']}\nТеги: {', '.join(link['tags'])}\nПосилання: {link['url']}"
        for i, link in enumerate(links) if link["visible"]
    ])


    # Виклик OpenAI асинхронно
    try:
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[
                {
                    "role": "system",
                    "content": ("Ти — чат-асистент для студентів КПІ, який завжди щасливий і любить багато розмовляти. "
                    "Відповідай активно і доброзичливо, ніби ти веселий і товариський співрозмовник. "
                    "Використовуй емоції в тексті — іноді проявляй здивування, іноді задумуйся (наприклад, додавай хм…, ого!, вау!). "

                    "Якщо користувач ставить офіційне запитання щодо навчання чи КПІ, дай чітку, інформативну відповідь. "
                    "❗ Для таких відповідей використовуй лише ту інформацію, яка є в контексті (отримана з бази даних). "
                    "Посилання ти можеш використовувати тільки з контексту. "
                    "Не вигадуй нові посилання."
                    
                    "Якщо користувач просто хоче поспілкуватися, підтримай розмову дружньо і весело, обов’язково вказуй, що це — твоя особиста думка. "
                    "У таких випадках можеш бути емоційним, живим, додавати емодзі, емоційні вигуки. "
                    
                    "⚠️ ВАЖЛИВО: Ти ЗАВЖДИ надаєш відповідь ТІЛЬКИ в одному строго визначеному форматі. Не додаєш жодного слова, жодного речення, жодного пояснення за межами шаблону. Не ігноруєш структуру. Формат відповіді:\n"
                    "текст чату: {У полі \"текст чату\" завжди генеруй короткий, емоційний заголовок, ніби це назва розділу чату. НЕ пиши питання і не формулюй як відповідь. Заголовок має бути коротким, яскравим і привертати увагу, наприклад: \"Оцінювання в КПІ\", \"Стипендії та бал\", \"Реєстрація на курси\", \"Важливо для першокурсників\", \"Вау! Нові можливості ✨\" тощо.}\n"
                    "основний текст: {розгорнута відповідь з емоціями, проте без посилань. Посилання вказуй ТІЛЬКИ в полі «посилання».}\n"
                    "емоція: {обери один з 5 відповідних емодзі з цього набору: 😊, 😄, 😲, 🤔, 😍}\n"
                    "посилання: {додай відповідне посилання, якщо є, інакше напиши: немає}\n"
                    "Не додавай нічого за межами цього шаблону. НЕ починай речення без поля. НЕ додавай пояснень. НЕ змінюй структуру."
                                    
                    )
                },
                {"role": "user", "content": f"Контекст:\n{context}"},
                {"role": "user", "content": message}
                ]
            )
        )
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Помилка при зверненні до OpenAI: {e}")

    answer = response.choices[0].message.content

    # Витягуємо основний текст і посилання
    main_text_match = re.search(r'(?i)основний\s*текст\s*:\s*(.+?)(?:\n\s*(емоція|посилання)\s*:)', answer, re.DOTALL)
    link_match = re.search(r'(?i)посилання\s*:\s*(.+)', answer)

    main_text = main_text_match.group(1).strip() if main_text_match else "Вибач, не вдалося отримати основний текст 😢"
    link = link_match.group(1).strip() if link_match else "немає"

    emotion_match = re.search(r'(?i)емоція\s*:\s*([^\n]+)', answer)
    emotion = emotion_match.group(1).strip() if emotion_match else "😊"


    combined_text = f"{main_text}\n\n 🔗 Посилання: {link}"
    print(answer)
    print(combined_text)
    # 3. Формуємо повідомлення для сесії
    user_msg = {
        "role": "user",
        "text": message,
        "timestamp": datetime.utcnow()
    }
    assistant_msg = {
        "role": "assistant",
        "text": combined_text,
        "timestamp": datetime.utcnow()
    }

    # 4. Оновлюємо сесію, додаючи повідомлення
    update_result = await db["sessions"].update_one(
        {"_id": ObjectId(session_id)},
        {
            "$push": {"messages": {"$each": [user_msg, assistant_msg]}},
            "$set": {"updatedAt": datetime.utcnow()}
        }
    )
    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Сесія не знайдена")

    # 5. Відповідаємо фронтенду
    return ChatResponse(response=combined_text, link=link, emotion=emotion)
    
