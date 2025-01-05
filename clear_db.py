import sqlite3

def clear_database():
    conn = sqlite3.connect("volunteers.db")
    cursor = conn.cursor()

    try:
        cursor.execute("BEGIN")
        cursor.execute("DELETE FROM users")
        conn.commit()
        print("База данных очищена.")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка при очистке базы данных: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    clear_database()
