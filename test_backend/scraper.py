# # Файл який за посиланням дістає інформацію зі сторінки

# import requests
# from bs4 import BeautifulSoup
# import sys
# import io

# # Встановлення кодування для стандартного виведення
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# # URL сторінки з викладачами
# url = 'https://iate.kpi.ua/ua/127-vikladackiy-sklad-kafedra-inzhenerii-programnogo-zabezpechennya-v-energetici'

# # Надсилаємо GET-запит до сторінки
# response = requests.get(url)
# response.encoding = 'utf-8'  # Встановлюємо правильне кодування

# # Перевіряємо, чи запит був успішним
# if response.status_code == 200:
#     # Створюємо об'єкт BeautifulSoup для парсингу HTML
#     soup = BeautifulSoup(response.text, 'html.parser')

#     # Знаходимо всі елементи, які містять інформацію про викладачів
#     # Припустимо, що кожен викладач знаходиться в елементі <p>
#     paragraphs = soup.find_all('p')

#     # Виводимо текст кожного абзацу
#     for p in paragraphs:
#         print(p.get_text(strip=True))
# else:
#     print(f"Помилка при отриманні сторінки: {response.status_code}")


import requests
from bs4 import BeautifulSoup
import sys
import io
# Встановлення кодування для стандартного виведення
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def get_page_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    paragraphs = soup.find_all('p')
    info_text = "\n".join(p.get_text(strip=True) for p in paragraphs)
    return info_text
