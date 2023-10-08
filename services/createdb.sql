CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code VARCHAR(32),
            name VARCHAR(30),
            tg_id INT,
            role VARCHAR(15));