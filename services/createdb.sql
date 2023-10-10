CREATE TABLE IF NOT EXISTS users
(
    tg_id INTEGER PRIMARY KEY,
    code  VARCHAR(32),
    name  VARCHAR(30),
    role  VARCHAR(15)
);

CREATE TABLE IF NOT EXISTS tasks
(
    task_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    users_tg_id INTEGER,
    date_added  DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date    DATE,
    task_text   TEXT,
    FOREIGN KEY (users_tg_id) REFERENCES users (tg_id)
);
