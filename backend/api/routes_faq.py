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

router = APIRouter(prefix="/api/faq", tags=["FAQ"])

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",  # ✅ OpenRouter endpoint
    api_key="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",  
    http_client=Client(trust_env=False)# 🔑 Встав сюди свій особистий API-ключ з https://openrouter.ai
)

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

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat_with_faq(request: ChatRequest, db=Depends(get_database)):
    message = request.message.lower()
    print("123")
    # Пошук FAQ релевантних
    faqs = await faq_model.get_all_faqs(db)
    relevant = []
    for faq in faqs:
        if message in faq["question"].lower() or message in faq["answer"].lower():
            relevant.append(faq)
            if len(relevant) >= 3:  # максимум 3 для контексту
                break

    # Формуємо контекст
    context = "\n\n".join([
        f"Питання: {item['question']}\nВідповідь: {item['answer']}\nДжерело: {item.get('source', 'немає')}"
        for item in relevant
    ])

    # Виклик OpenAI асинхронно
    try:
        response = await asyncio.to_thread(
            lambda: client.chat.completions.create(
                model="google/gemma-3-4b-it:free",
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
                    
                    "⚠️ Форматуй свою відповідь ТІЛЬКИ в такому вигляді:\n"
                    "текст чату: {ккороткий заголовок або емоційний вступ, який відображатиметься як заголовок чату або прев’ю повідомлення. Зроби його помітним, емоційним, таким, щоб привертав увагу користувача.}\n"
                    "основний текст: {розгорнута відповідь з емоціями}\n"
                    "емоція: {обери до 5 відповідних емодзі з цього набору: 😊, 😄, 😲, 🤔, 😍}\n"
                    "посилання: {додай відповідне посилання, якщо є, інакше напиши: немає}\n"
                    "Не додавай нічого поза цим шаблоном. Не пояснюй свій вибір."
                                    
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
    print(answer)
    # Пошук незалежно від регістру та пробілів
    main_text_match = re.search(r'(?i)основний\s*текст\s*:\s*(.+?)(?:\n\s*(емоція|посилання)\s*:)', answer, re.DOTALL)
    link_match = re.search(r'(?i)посилання\s*:\s*(.+)', answer)

    main_text = main_text_match.group(1).strip() if main_text_match else "Вибач, не вдалося отримати основний текст 😢"
    link = link_match.group(1).strip() if link_match else "немає"

    return ChatResponse(response=main_text, link=link)
    
