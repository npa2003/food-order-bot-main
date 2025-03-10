# -*- coding: utf-8 -*-
import sqlite3
from test import *
import os

# Указываем абсолютный путь к базе данных
db_name = os.path.join(os.path.dirname(__file__), "db", "food_orders.db")
print (db_name)
# db_name = 'db/food_orders.db'

@print_function_name
def add_user(telegram_id, username, first_name, last_name):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (telegram_id, username, first_name, last_name) VALUES (?, ?, ?, ?)", (telegram_id, username, first_name, last_name,))
    conn.commit()
    conn.close()

@print_function_name
def add_user_adr(id, adress):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET adress = ? WHERE telegram_id = ?", (adress, id))
    conn.commit()
    conn.close()

@print_function_name        # достаём адрес доставки по id
def get_user_adr(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT adress FROM users WHERE telegram_id = ?",(user_id,))
    result = cursor.fetchall()
    conn.close()
    #print(f'Результат: {result}')
    return result

@print_function_name
def get_restaurants():
    #print(db_name)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description, logo FROM restaurants")
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "description": row[2], "logo": row[3]} for row in result]

@print_function_name
def get_categories(restaurant_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name FROM categories WHERE restaurant_id = ?", (restaurant_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1]} for row in result]

@print_function_name
def get_dishes(category_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, price, description FROM dishes WHERE category_id = ?", (category_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"id": row[0], "name": row[1], "price": row[2], "description": row[3]} for row in result]

@print_function_name
def add_to_cart(user_id, dish_id, price, restaurant_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM orders WHERE user_id = ? AND status = 'new'", (user_id,))
    order = cursor.fetchone()

    if order is None:
        cursor.execute("INSERT INTO orders (user_id, restaurant_id, status, total_cost) VALUES (?, ?, 'new', 0)",
                       (user_id, restaurant_id))
        order_id = cursor.lastrowid
    else:
        order_id = order[0]

    cursor.execute("SELECT id, quantity FROM order_items WHERE order_id = ? AND dish_id = ?", (order_id, dish_id))
    item = cursor.fetchone()

    if item is None:
        cursor.execute(
            "INSERT INTO order_items (order_id, dish_id, quantity, price, total) VALUES (?, ?, 1, ?, ?)",
            (order_id, dish_id, price, price))
        cursor.execute("UPDATE orders SET total_cost = total_cost + ? WHERE id = ?", (price, order_id))
    else:
        new_quantity = item[1] + 1
        new_total = new_quantity * price
        cursor.execute("UPDATE order_items SET quantity = ?, total = ? WHERE id = ?",
                       (new_quantity, new_total, item[0]))
        cursor.execute("UPDATE orders SET total_cost = total_cost + ? WHERE id = ?", (price, order_id))

    conn.commit()
    conn.close()

@print_function_name
def get_cart(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT dishes.name AS dish_name, quantity, total FROM order_items "
                   "INNER JOIN dishes ON order_items.dish_id = dishes.id "
                   "WHERE order_id IN (SELECT id FROM orders WHERE user_id = ? AND status = 'new')", (user_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"dish_name": row[0], "quantity": row[1], "total": row[2]} for row in result]


@print_function_name
def change_order_status(user_id, status):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET status = ? WHERE user_id = ? AND status = 'new' OR status = 'confirmed'", (status, user_id))
    conn.commit()
    conn.close()

@print_function_name
def change_order_payment_method(order_id, payment_method):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("UPDATE orders SET payment_method = ? WHERE id = ? AND status = 'paid' OR status = 'confirmed'", (payment_method, order_id))
    conn.commit()
    conn.close()

@print_function_name
def get_user_orders(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT status, total_cost, payment_method, DATE(order_date) AS updated_at FROM orders WHERE user_id = ? AND status != 'new'",
                   (user_id,))
    result = cursor.fetchall()
    conn.close()
    return [{"status": row[0], "total_cost": row[1], "payment_method": row[2], "updated_at": row[3]} for row in result]


@print_function_name
def get_current_order_id(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM orders WHERE user_id = ? AND status = 'confirmed'", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0]

@print_function_name
def get_user_orders_fb(user_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT id, user_id, restaurant_id, status, total_cost, payment_method, DATE(order_date) AS updated_at FROM orders WHERE user_id = ? AND status != 'completed'", (user_id,))
    result = cursor.fetchall()
    #print(result)
    conn.close()
    return [{"id": row[0],
             "user_id": row[1],
             "restaurant_id": row[2],
             "status": row[3],
             "total_cost": row[4],
             "payment_method": row[5],
             "updated_at": row[6]}
            for row in result]

@print_function_name
def add_fb(telegram_id, data_fb, fb_t, fb_r):
    #print(data_fb)
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reviews (user_id, restaurant_id, order_id, comment, rating) VALUES (?, ?, ?, ?, ?)",
                    (telegram_id, data_fb['restaurant_id'], data_fb['id'], fb_t, fb_r))
    conn.commit()
    conn.close()

@print_function_name
def get_rest_fb(restaurant_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT AVG(rating), COUNT(rating) FROM reviews WHERE restaurant_id = ?", (restaurant_id,))
    result = cursor.fetchone()
    conn.close()
    return result

@print_function_name
def get_username(telegram_id):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT first_name FROM users WHERE telegram_id = ?", (telegram_id,))
    result = cursor.fetchone()
    conn.close()
    return result