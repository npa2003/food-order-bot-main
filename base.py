import sqlite3


def init_db():
    conn = sqlite3.connect("order_bot.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            telegram_id INTEGER PRIMARY KEY,
            username TEXT,                          -- имя пользователя (никнейм)
            first_name TEXT,
            last_name TEXT,
            address TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

def add_user(telegram_id, username, first_name, last_name):
    conn = sqlite3.connect("order_bot.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Users (telegram_id, username, first_name, last_name, address) VALUES (?, ?, ?, ?, NULL)", (telegram_id, username, first_name, last_name,))
    conn.commit()
    conn.close()