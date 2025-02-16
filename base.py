import sqlite3


def add_user(telegram_id, username, first_name, last_name):
    conn = sqlite3.connect("db/food_orders")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO Users (telegram_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", (telegram_id, username, first_name, last_name,))
    conn.commit()
    conn.close()

def get_restaurants():
    conn = sqlite3.connect("db/food_orders")
    cursor = conn.cursor()
    cursor.execute("SELECT name, description FROM restaurants")
    result = cursor.fetchall()
    conn.close()
    return [{"name": row[0], "description": row[1]} for row in result]