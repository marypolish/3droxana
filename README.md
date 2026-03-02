## 3droxana — AI‑чат для студентів

3droxana — це веб‑застосунок з FastAPI‑бекендом і статичним фронтендом, який надає **розумного чат‑асистента для студентів**:

- **Пояснює правила та процеси навчання** (предмети, реєстрація, оцінювання, стипендії тощо).
- **Підказує корисні ресурси** з бази посилань коледжу / університету.
- **Веде історію сесій спілкування**, щоб можна було повертатись до попередніх діалогів.

Бекенд працює поверх FastAPI, зберігає дані у MongoDB і викликає зовнішню LLM‑модель (через Together API).

---

## Вимоги

- Python 3.12+
- Git Bash **або** інший bash‑сумісний термінал на Windows
- Доступ до MongoDB (локальний або MongoDB Atlas)

---

## Локальний запуск (Git Bash, venv)

### 1. Клонувати репозиторій та перейти в папку проєкту

```bash
git clone <URL-репозиторію>
cd 3droxana
```

### 2. Створити віртуальне середовище (один раз)

```bash
py -3 -m venv venv   # або: python -m venv venv
```

### 3. Активувати venv у Git Bash

```bash
source venv/Scripts/activate
```

У рядку термінала має з’явитися префікс `(venv)`.

### 4. Встановити залежності

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 5. Налаштувати секрети через `.env`

У корені проєкту створіть файл `.env` (він уже доданий у `.gitignore`, тому не потрапить у git) з таким вмістом **(значення замініть на свої)**:

```env
MONGODB_URI="mongodb+srv://polishchukmariyatv21:LspA8MqTknfK535S@3davatar.jd7ic5f.mongodb.net/"
DATABASE_NAME="3davatar"
TOGETHER_API_KEY="137f302b0bb50bb26cbf1f491b2bf183bf54c1bebd7df461ac9d0441f8f7f9d7"
```

- `MONGODB_URI` — повний URI до вашого MongoDB/Atlas‑кластера.
- `DATABASE_NAME` — назва бази, за замовчуванням використовується `3davatar`.
- `TOGETHER_API_KEY` — API‑ключ від Together (для LLM‑моделі).

### 6. Запустити сервер

```bash
python -m uvicorn backend.main:app --reload --port 8000
```

Після запуску API та фронтенд будуть доступні за адресою:

- `http://localhost:8000` — основна сторінка застосунку.

---

## Запуск через Docker

### 1. Збірка образу

```bash
docker build -t 3droxana .
```

### 2. Запуск контейнера з секретами

Рекомендовано передавати ті ж самі змінні оточення, що й у `.env`:

```bash
docker run -p 8000:8000 \
  -e MONGODB_URI="mongodb+srv://polishchukmariyatv21:LspA8MqTknfK535S@3davatar.jd7ic5f.mongodb.net/" \
  -e DATABASE_NAME="3davatar" \
  -e TOGETHER_API_KEY="137f302b0bb50bb26cbf1f491b2bf183bf54c1bebd7df461ac9d0441f8f7f9d7" \
  3droxana
```

Після цього застосунок буде доступний на `http://localhost:8000`.

---

## Коротко про структуру

- `backend/` — FastAPI‑бекенд (роути, моделі, робота з MongoDB).
- `assistant_core/` — бізнес‑логіка чат‑асистента (виклики LLM, парсинг відповіді, оновлення сесій).
- `frontend/` — статичні HTML/CSS/JS‑сторінки для інтерфейсу.
- `avatar/` — медіафайли для 3D‑/анімаційного аватара.
- `requirements.txt` — список Python‑залежностей.
- `Dockerfile` — опис Docker‑образу для продакшен/контейнерного запуску.
- `.env` — **локальні секрети** (не комітяться в git).
