import sqlite3

conn = sqlite3.connect('databases/database.db')
cursor = conn.cursor()


def insert(table: str, data_dict: dict) -> None:
    """Добавляет данные в таблицу"""
    columns = ', '.join(data_dict.keys())
    values = [tuple(data_dict.values())]
    placeholders = ', '.join('?' * len(data_dict))
    cursor.executemany(
        f'INSERT INTO {table} '
        f'({columns}) '
        f'VALUES ({placeholders})',
        values)
    conn.commit()


async def update_auth(tg_id, value):
    """Устанавливает поле auth на True"""
    try:
        query = 'UPDATE users SET auth = ? WHERE tg_id = ?;'
        cursor.execute(query, (value, tg_id))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


def auth_status(tg_id: int):
    try:
        query = "SELECT auth FROM users WHERE tg_id = ?;"
        cursor.execute(query, (tg_id,))
        result = cursor.fetchone()

        if result:
            auth_value, *_ = result
            return auth_value
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


def fetch_users_db(arg: str) -> list[str] | None:
    """Выводит список значений выбранного аргумента"""
    try:
        cursor.execute(f'SELECT {arg} FROM users')
        rows = [arg for rows in cursor.fetchall() for arg in rows]
        return rows
    except sqlite3.Error as e:
        print('Ошибка при извлечении данных:', e)


# временная <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
async def clear_users_table():
    try:
        cursor.execute("DELETE FROM users")

        conn.commit()
        conn.close()
        print('Таблица users успешно очищена.')
    except sqlite3.Error as e:
        print('Ошибка при очистке таблицы:', e)


def get_cursor():
    return cursor


def _init_db() -> None:
    """Инициализирует БД"""
    with open('services/createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute('SELECT name FROM sqlite_master '
                   'WHERE type="table" AND name="users"')
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
