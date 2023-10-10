import sqlite3

conn = sqlite3.connect('databases/database.db')
cursor = conn.cursor()


def insert_data_from_dict(data_dict: dict) -> None:
    """Заносит данные о новом пользователе в таблицу users"""
    try:
        cursor.execute("INSERT INTO users (tg_id, code, name, role) "
                       "VALUES (?, ?, ?, ?)",
                       (data_dict.get('tg_id'), data_dict.get('code'), data_dict.get('name'), data_dict.get('role')))

        conn.commit()
        print("New user add to table")
    except sqlite3.Error as e:
        print("Add error:", e)


def fetch_codes() -> list[str] | None:
    """Выводит список выданных кодов доступа"""
    try:
        cursor.execute("SELECT code FROM users")
        rows = [code for rows in cursor.fetchall() for code in rows]
        return rows
    except sqlite3.Error as e:
        print("Ошибка при извлечении данных:", e)


async def clear_users_table():
    try:
        cursor.execute("DELETE FROM users")

        conn.commit()
        conn.close()
        print("Таблица 'users' успешно очищена.")
    except sqlite3.Error as e:
        print("Ошибка при очистке таблицы:", e)


def insert_task(data_dict: dict) -> None:
    """Заносит данные о задаче в таблицу tasks"""
    try:
        cursor.execute("INSERT INTO tasks (user_tg_id, due_date, task_text) "
                       "VALUES (?, ?, ?)",
                       (data_dict.get('tg_id'), data_dict.get('code'), data_dict.get('name'), data_dict.get('role')))

        conn.commit()
        print("New user add to table")
    except sqlite3.Error as e:
        print("Add error:", e)


def _init_db() -> None:
    """Инициализирует БД"""
    with open("services/createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='users'")
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
