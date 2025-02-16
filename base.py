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
    cursor.execute("SELECT id, name, description, logo FROM restaurants")
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "description": row[2], "logo": row[3]} for row in result]

def get_categories(restaurant_id):
    conn = sqlite3.connect("db/food_orders")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE restaurant_id = ?", (restaurant_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in result]

def get_dishes(category_id):
    conn = sqlite3.connect("db/food_orders")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description FROM dishes WHERE category_id = ?", (category_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "price": row[2], "description": row[3]} for row in result]