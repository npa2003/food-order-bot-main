import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
from base import *

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


restaurants = get_restaurants()

soups = [
    {"name": "Борщ", "photo": "https://aif-s3.aif.ru/images/028/368/b4e33f182b30c9ce94fca1f35f4bd2a1.jpg", "price": 250},
    {"name": "Солянка", "photo": "https://ferma-alpatevo.ru/image/cache/catalog/2/soup/186-auto_width_1000.jpg", "price": 300}
]

current_index = 0
current_soup_index = 0
order = {"items": [], "total_price": 0}
completed_orders = {}
user_addresses = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Старт")
    keyboard.add(start_button)
    bot.send_message(message.chat.id, "Нажмите 'Старт', чтобы начать", reply_markup=keyboard)


@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    add_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    username = message.from_user.first_name
    text = f"Привет, {username}! Я бот, который поможет тебе заказать еду."
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(message.chat.id, text, reply_markup=inline_keyboard)

@bot.message_handler(func=lambda message: message.text == "Личный кабинет")
def profile_button_handler(message):
    send_user_profile(message.chat.id, message.from_user.id)


@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    global current_index, current_soup_index, order
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == "choose_restaurant":
        current_index = 0
        send_restaurant_info(call.message.chat.id)
    elif call.data == "prev_restaurant":
        current_index = (current_index - 1) % len(restaurants)
        send_restaurant_info(call.message.chat.id)
    elif call.data == "next_restaurant":
        current_index = (current_index + 1) % len(restaurants)
        send_restaurant_info(call.message.chat.id)
    elif call.data == "select_restaurant":
        send_menu(call.message.chat.id)
    elif call.data == "soups":
        current_soup_index = 0
        send_soup_info(call.message.chat.id)
    elif call.data == "prev_soup":
        current_soup_index = (current_soup_index - 1) % len(soups)
        send_soup_info(call.message.chat.id)
    elif call.data == "next_soup":
        current_soup_index = (current_soup_index + 1) % len(soups)
        send_soup_info(call.message.chat.id)
    elif call.data == "add_soup":
        order["items"].append(soups[current_soup_index])
        order["total_price"] += soups[current_soup_index]["price"]
        send_soup_info(call.message.chat.id)
    elif call.data == "cart":
        send_cart(call.message.chat.id)
    elif call.data == "back_to_start":
        handle_start(call.message)
    elif call.data == "confirm_order":
        send_payment_options(call.message.chat.id)
    elif call.data == "pay_online":
        process_online_payment(call.message.chat.id, call.from_user.id)
    elif call.data == "profile":
        send_user_profile(call.message.chat.id, call.from_user.id)


def send_restaurant_info(chat_id):
    inline_keyboard = InlineKeyboardMarkup()
    btn_prev = InlineKeyboardButton("Пред.", callback_data="prev_restaurant")
    btn_next = InlineKeyboardButton("След.", callback_data="next_restaurant")
    btn_select = InlineKeyboardButton("Выбрать", callback_data="select_restaurant")
    btn_back = InlineKeyboardButton("Назад", callback_data="back_to_start")
    inline_keyboard.row(btn_prev, btn_next)
    inline_keyboard.row(btn_select)
    inline_keyboard.row(btn_back)
    # bot.send_photo(chat_id, restaurants[current_index]["logo"], caption=restaurants[current_index]["name"],
#                   reply_markup=inline_keyboard)
    bot.send_message(chat_id, restaurants[current_index]["name"], reply_markup=inline_keyboard)


def send_menu(chat_id):
    inline_keyboard = InlineKeyboardMarkup()
    btn_soups = InlineKeyboardButton("Супы", callback_data="soups")
    btn_salads = InlineKeyboardButton("Салаты", callback_data="salads")
    btn_hot_dishes = InlineKeyboardButton("Горячие блюда", callback_data="hot_dishes")
    btn_drinks = InlineKeyboardButton("Напитки", callback_data="drinks")
    btn_back = InlineKeyboardButton("Назад", callback_data="choose_restaurant")
    inline_keyboard.row(btn_soups, btn_salads)
    inline_keyboard.row(btn_hot_dishes, btn_drinks)
    inline_keyboard.row(btn_back)
    bot.send_photo(chat_id, restaurants[current_index]["logo"], caption=restaurants[current_index]["name"],
                   reply_markup=inline_keyboard)


def send_soup_info(chat_id):
    inline_keyboard = InlineKeyboardMarkup()
    btn_prev = InlineKeyboardButton("Пред.", callback_data="prev_soup")
    btn_next = InlineKeyboardButton("След.", callback_data="next_soup")
    btn_add = InlineKeyboardButton("Добавить в заказ", callback_data="add_soup")
    btn_cart = InlineKeyboardButton("Корзина", callback_data="cart")
    btn_back = InlineKeyboardButton("Назад", callback_data="select_restaurant")
    inline_keyboard.row(btn_prev, btn_next)
    inline_keyboard.row(btn_add)
    inline_keyboard.row(btn_cart, btn_back)
    bot.send_photo(chat_id, soups[current_soup_index]["photo"],
                   caption=f"{soups[current_soup_index]['name']} - {soups[current_soup_index]['price']} руб.",
                   reply_markup=inline_keyboard)


def send_cart(chat_id):
    if not order["items"]:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    text = "Ваш заказ:\n"
    for item in order["items"]:
        text += f"{item['name']} - {item['price']} руб.\n"
    text += f"\nОбщая стоимость: {order['total_price']} руб."
    inline_keyboard = InlineKeyboardMarkup()
    btn_confirm = InlineKeyboardButton("Подтвердить заказ", callback_data="confirm_order")
    btn_back = InlineKeyboardButton("Назад", callback_data="soups")
    inline_keyboard.row(btn_confirm)
    inline_keyboard.row(btn_back)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

def send_payment_options(chat_id):
    if not order["items"]:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    text = "Ваш заказ:\n"
    for item in order["items"]:
        text += f"{item['name']} - {item['price']} руб.\n"
    text += f"\nОбщая стоимость: {order['total_price']} руб."
    text += "\nВыберите способ оплаты:"
    inline_keyboard = InlineKeyboardMarkup()
    btn_online = InlineKeyboardButton("Оплата онлайн", callback_data="pay_online")
    btn_cash = InlineKeyboardButton("Оплата наличными", callback_data="pay_cash")
    inline_keyboard.row(btn_online, btn_cash)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

def process_online_payment(chat_id, user_id):
    if user_id not in completed_orders:
        completed_orders[user_id] = []
    completed_orders[user_id].append(order.copy())
    bot.send_message(chat_id, "Оплата прошла успешно! Ваш заказ оформлен.")
    order["items"].clear()
    order["total_price"] = 0

def send_user_profile(chat_id, user_id):
    address = user_addresses.get(user_id, "Введите адрес доставки")
    text = f"Имя пользователя: {user_id}\nАдрес доставки: {address}"
    inline_keyboard = InlineKeyboardMarkup()
    btn_orders = InlineKeyboardButton("История заказов", callback_data="order_history")
    btn_back = InlineKeyboardButton("Назад", callback_data="back_to_start")
    inline_keyboard.row(btn_orders)
    inline_keyboard.row(btn_back)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

#init_db()
bot.polling(none_stop=True)
