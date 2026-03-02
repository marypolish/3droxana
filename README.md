# 3droxana

Застосунок з FastAPI-бекендом та статичним фронтендом. Нижче — як розгорнути його через Docker.

---

## Що потрібно

- [Docker](https://docs.docker.com/get-docker/) (встановлений і запущений на машині)
- Доступ до MongoDB (локальний або MongoDB Atlas)

---

## Розгортання через Dockerfile

### 1. Клонування та перехід у папку проєкту

```bash
git clone <URL-репозиторію> 3droxana
cd 3droxana
```

(Якщо проєкт уже є локально — просто перейди в його кореневу папку.)

### 2. Збірка образу

У корені проєкту (де лежать `Dockerfile` і `requirements.txt`):

```bash
docker build -t 3droxana .
```

- `-t 3droxana` — ім’я образу (можна змінити).
- Крапка в кінці — контекст збірки (поточна папка).

### 3. Запуск контейнера

**Базовий запуск** (MongoDB беруться з `backend/config.py`):

```bash
docker run -p 8000:8000 3droxana
```

- `-p 8000:8000` — порт контейнера 8000 проброшується на хост.
- Застосунок буде доступний: **http://localhost:8000**

**З указанням MongoDB через змінні оточення** (рекомендовано для продакшену):

```bash
docker run -p 8000:8000 \
  -e MONGODB_URI="mongodb+srv://user:pass@cluster.mongodb.net/" \
  -e DATABASE_NAME="3davatar" \
  3droxana
```

На Windows (PowerShell) можна в один рядок:

```powershell
docker run -p 8000:8000 -e MONGODB_URI="mongodb+srv://..." -e DATABASE_NAME="3davatar" 3droxana
```

### 4. Зупинка та видалення

- Зупинити контейнер: `Ctrl+C` у терміналі, де він запущений, або в іншому терміналі:
  ```bash
  docker stop $(docker ps -q --filter ancestor=3droxana)
  ```
- Видалити контейнер після зупинки (за потреби): через `docker rm <container_id>` або Docker Desktop.

---

## Корисні команди

| Дія | Команда |
|-----|--------|
| Зібрати образ без кешу | `docker build --no-cache -t 3droxana .` |
| Запустити у фоні (detached) | `docker run -d -p 8000:8000 --name 3droxana-app 3droxana` |
| Переглянути логи | `docker logs 3droxana-app` (або ID контейнера) |
| Зупинити контейнер за іменем | `docker stop 3droxana-app` |

---

## Структура проєкту (що потрібно для Docker)

- `Dockerfile` — опис образу (Python 3.12, залежності, копіювання `backend/`, `frontend/`, `avatar/`).
- `requirements.txt` — Python-залежності бекенду.
- `.dockerignore` — виключає `venv`, `.git`, кеш тощо при збірці.

Якщо потрібно змінити порт або додати змінні оточення — змінюй аргументи в `docker run` або (краще) використовуй `docker-compose.yml` для зручної конфігурації.
