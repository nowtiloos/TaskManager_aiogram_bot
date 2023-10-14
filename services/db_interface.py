import sqlite3

db = sqlite3.connect('databases/database.db')
cursor = db.cursor()


def insert(table: str, data_dict: dict) -> None:
    """Добавляет данные в таблицу"""
    columns = ', '.join(data_dict.keys())
    values = [tuple(data_dict.values())]
    placeholders = ', '.join('?' * len(data_dict))
    try:
        with db:
            db.executemany(
                f'INSERT INTO {table} '
                f'({columns}) '
                f'VALUES ({placeholders})',
                values)
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных: {e}")


def fetch_codes() -> list[str] | None:
    """Выводит список значений code из таблицы users"""
    try:
        with db:
            cursor.execute(f'SELECT code FROM users;')
            rows: list[str] = [arg for rows in cursor.fetchall() for arg in rows]
            return rows
    except sqlite3.Error as e:
        print('Ошибка при извлечении данных:', e)


async def update_auth(tg_id, value):
    """Устанавливает поле auth на True"""
    try:
        with db:
            query = 'UPDATE users SET auth = ? WHERE tg_id = ?;'
            cursor.execute(query, (value, tg_id))
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


def auth_status(tg_id: int):
    try:
        with db:
            query = "SELECT auth FROM users WHERE tg_id = ?;"
            cursor.execute(query, (tg_id,))
            result = cursor.fetchone()
            if result:
                auth_value, *_ = result
                return auth_value
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


async def clear_table(table: str) -> None:
    """Очищает таблицу"""
    try:
        with db:
            cursor.execute(f'DELETE FROM {table};')
            print(f'Таблица {table} успешно очищена.')
    except sqlite3.Error as e:
        print('Ошибка при очистке таблицы:', e)


def _init_db() -> None:
    """Инициализирует БД"""
    with open('services/createdb.sql', 'r') as f:
        with db:
            sql = f.read()
        cursor.executescript(sql)
    print('database init')


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    with db:
        cursor.execute('SELECT name FROM sqlite_master '
                       'WHERE type="table" AND name="users";')
        table_exists = cursor.fetchall()
        if table_exists:
            return
        _init_db()


check_db_exists()
