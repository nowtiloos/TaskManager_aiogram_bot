import sqlite3

db = sqlite3.connect('databases/database.db')
cursor = db.cursor()


def insert(table: str, data_dict: dict) -> None:
    """Добавляет данные в таблицу"""
    columns = ', '.join(data_dict.keys())
    values = [tuple(data_dict.values())]
    placeholders = ', '.join('?' * len(data_dict))
    try:
        cursor.executemany(
            f'INSERT INTO {table} '
            f'({columns}) '
            f'VALUES ({placeholders})',
            values)
        db.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при вставке данных: {e}")


async def update_auth(tg_id, value):
    """Устанавливает поле auth на True"""
    try:
        query = 'UPDATE users SET auth = ? WHERE tg_id = ?;'
        cursor.execute(query, (value, tg_id))
        db.commit()
    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


async def clear_table(table: str, condition=None) -> None:
    """Очищает таблицу"""
    try:
        query = f'DELETE FROM {table};'

        if condition:
            query += f' WHERE {condition}'

        cursor.execute(query)
        db.commit()
        print(f'Таблица {table} успешно очищена.')
    except sqlite3.Error as e:
        print('Ошибка при очистке таблицы:', e)


def query_database(table: str, columns: tuple[str, ...], condition=None, group_by=None, order_by=None):
    """Осуществляет запрос к базе данных"""
    try:
        query = f'SELECT {",".join(columns)} FROM {table}'

        if condition:
            query += f' WHERE {condition}'
        if group_by:
            query += f' GROUP BY {group_by}'
        if order_by:
            query += f' ORDER BY {order_by}'

        cursor.execute(query)
        data: list[table] = cursor.fetchall()

        return data

    except sqlite3.Error as e:
        print(f"Ошибка SQLite: {e}")


def _init_db() -> None:
    """Инициализирует БД"""
    with open('services/createdb.sql', 'r') as f:
        sql = f.read()
    cursor.executescript(sql)
    db.commit()
    print('db init')


def check_db_exists() -> None:
    """Проверяет, инициализирована ли БД, если нет — инициализирует"""
    cursor.execute('SELECT name FROM sqlite_master '
                   'WHERE type="table" AND name="users";')
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
