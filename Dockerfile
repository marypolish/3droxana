# 3droxana — FastAPI backend + static frontend
FROM python:3.12-slim

WORKDIR /app

# Залежності
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Код проєкту (backend, frontend, avatar)
COPY backend ./backend
COPY frontend ./frontend
COPY avatar ./avatar

# Порт
EXPOSE 8000

# MONGODB_URI та DATABASE_NAME можна передати через -e при docker run
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
