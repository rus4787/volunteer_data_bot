import sqlite3
from datetime import datetime

# Создание и подключение к базе данных
def init_db():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        # Создание таблицы users с полем user_id
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                nickname TEXT NOT NULL UNIQUE,
                competencies TEXT,
                roles TEXT,
                tracker_access BOOLEAN,
                timezone INTEGER,
                preferred_time TEXT,
                github TEXT,
                additional_data TEXT,
                form_status TEXT DEFAULT 'ошибка',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()  # Коммит транзакции
    except Exception as e:
        conn.rollback()  # Откат транзакции при ошибке
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        conn.close()

# Добавление пользователя
def add_user(user_id, nickname, competencies=None, roles=None, tracker_access=None, 
             timezone=None, preferred_time=None, github=None, additional_data=None, form_status='ошибка'):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        
        # Проверяем количество никнеймов для данного user_id
        cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = ?", (user_id,))
        nickname_count = cursor.fetchone()[0]
        
        if nickname_count >= 3:
            raise ValueError(f"Пользователь с user_id {user_id} уже имеет 3 никнейма.")
        
        # Добавляем нового пользователя
        cursor.execute("""
            INSERT INTO users (user_id, nickname, competencies, roles, tracker_access, timezone, 
                               preferred_time, github, additional_data, form_status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (user_id, nickname, competencies, roles, tracker_access, timezone, preferred_time, github, additional_data, form_status))
        conn.commit()
    except ValueError as e:
        conn.rollback()
        print(e)
    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"Ошибка при добавлении пользователя: {e}")
    finally:
        conn.close()


# Проверка существования пользователя
def user_exists(nickname):
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()
    
    try:
        cursor.execute("BEGIN")
        cursor.execute("SELECT 1 FROM users WHERE nickname = ?", (nickname,))
        result = cursor.fetchone()
        conn.commit()  # Коммит транзакции
    except Exception as e:
        conn.rollback()  # Откат транзакции при ошибке
        print(f"Ошибка при проверке пользователя: {e}")
        result = None
    finally:
        conn.close()
    return result is not None

# Тестовая функция
if __name__ == "__main__":
    init_db()
    print("База данных и таблица успешно созданы!")
