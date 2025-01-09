import os
import json
import sqlite3
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import asyncio


async def backup_to_google_sheets():
    try:
        # Загружаем JSON из переменной окружения
        credentials_json = os.getenv("GOOGLE_CREDENTIALS")
        if not credentials_json:
            raise ValueError("Переменная окружения GOOGLE_CREDENTIALS не найдена.")
        credentials_dict = json.loads(credentials_json)

        # Настраиваем авторизацию Google API
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
        client = await asyncio.to_thread(gspread.authorize, credentials)

        # Открываем Google Sheet
        sheet = await asyncio.to_thread(client.open_by_key, "1_3ST2jprIGxACQE6Q0C8hMdQOy-6cZdb9bZkK--BgVU")
        sheet = sheet.sheet1

        # Подключение к SQLite
        conn = sqlite3.connect("volunteers.db")
        cursor = conn.cursor()

        # Проверка существования таблицы `users`
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            raise ValueError("Таблица `users` не найдена в базе данных.")

        # Извлечение данных из таблицы
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Очистка Google Sheet
        await asyncio.to_thread(sheet.clear)

        # Запись заголовков
        headers = [desc[0] for desc in cursor.description]
        await asyncio.to_thread(sheet.append_row, headers)

        # Запись данных
        for row in rows:
            await asyncio.to_thread(sheet.append_row, row)

        # Запись времени завершения бэкапа
        await asyncio.to_thread(sheet.append_row, ["Бэкап завершён:", " ", f"Дата: {datetime.now()}"])

        print("Backup completed!")

    except Exception as e:
        print(f"Ошибка во время выполнения: {e}")

    finally:
        if 'conn' in locals():
            conn.close()
