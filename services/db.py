import sqlite3

conn = sqlite3.connect('databases/users_db.db')
cursor = conn.cursor()


def insert_data_from_dict(data_dict: dict) -> None:
    try:
        # Вставка данных в таблицу
        cursor.execute("INSERT INTO users (code, name, tg_id, role) VALUES (?, ?, ?, ?)",
                       (data_dict.get('code'), data_dict.get('name'), data_dict.get('tg_id'), data_dict.get('role')))

        conn.commit()
        print("New user add to table")
    except sqlite3.Error as e:
        print("Add error:", e)


def fetch_codes():
    try:
        # Выполняем SQL-запрос для извлечения данных
        cursor.execute("SELECT code FROM users")
        # Извлекаем все строки результата
        rows = [j for i in cursor.fetchall() for j in i]
        return rows
    except sqlite3.Error as e:
        print("Ошибка при извлечении данных:", e)


def init_db() -> None:
    """Инициализирует БД"""
    with open("services/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


init_db()
