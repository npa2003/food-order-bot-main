import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
from base import *

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


restaurants = get_restaurants()
dishes = {}

current_index = 0
current_dish_index = 0
category_id = None
#order = {"items": [], "total_price": 0}
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
    global current_index, current_dish_index, dishes, category_id
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data.startswith("category"):
        category_id = int(call.data.split("|")[1])
        current_dish_index = 0
        dishes = get_dishes(category_id)
        send_category_info(call.message.chat.id)

    elif call.data == "choose_restaurant":
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
    elif call.data == "prev_dish":
        current_dish_index = (current_dish_index - 1) % len(dishes)
        send_category_info(call.message.chat.id)
    elif call.data == "next_dish":
        current_dish_index = (current_dish_index + 1) % len(dishes)
        send_category_info(call.message.chat.id)
    elif call.data == "add_dish":
        add_to_cart(call.from_user.id, dishes[current_dish_index]["id"], dishes[current_dish_index]["price"], current_index)
        send_category_info(call.message.chat.id)
    elif call.data == "cart":
        send_cart(call.message.chat.id)
    elif call.data == "back_to_start":
        handle_start(call.message)
    elif call.data == "confirm_order":
        pass
        send_payment_options(call.message.chat.id)
    elif call.data == "pay_online":
        pass
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

    image_path = restaurants[current_index]["logo"]
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        bot.send_photo(chat_id, photo=image_data, caption=restaurants[current_index]["name"],
                       reply_markup=inline_keyboard)
    except Exception as e:
        print(f"Произошла ошибка: {e}")


def send_menu(chat_id):
    restaurant = restaurants[current_index]["id"]
    categories = get_categories(restaurant)
    inline_keyboard = InlineKeyboardMarkup()
    for button in categories:
        inline_keyboard.add(InlineKeyboardButton(button["name"], callback_data="category" + "|" + str(button["id"])))
    btn_back = InlineKeyboardButton("Назад", callback_data="choose_restaurant")
    inline_keyboard.row(btn_back)

    image_path = restaurants[current_index]["logo"]
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        bot.send_photo(chat_id, photo=image_data, caption=restaurants[current_index]["name"], reply_markup=inline_keyboard)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

    #bot.send_photo(chat_id, image_data, caption=restaurants[current_index]["name"], reply_markup=inline_keyboard)


def send_category_info(chat_id):
    inline_keyboard = InlineKeyboardMarkup()
    btn_prev = InlineKeyboardButton("Пред.", callback_data="prev_dish")
    btn_next = InlineKeyboardButton("След.", callback_data="next_dish")
    btn_add = InlineKeyboardButton("Добавить в заказ", callback_data="add_dish")
    btn_cart = InlineKeyboardButton("Корзина", callback_data="cart")
    btn_back = InlineKeyboardButton("Назад", callback_data="select_restaurant")
    inline_keyboard.row(btn_prev, btn_next)
    inline_keyboard.row(btn_add)
    inline_keyboard.row(btn_cart, btn_back)
    # bot.send_photo(chat_id, dishes[current_dish_index]["photo"],
    #                caption=f"{dishes[current_dish_index]['name']} - {dishes[current_dish_index]['price']} руб.",
    #                reply_markup=inline_keyboard)
    bot.send_message(chat_id, f"{dishes[current_dish_index]['name']} - {dishes[current_dish_index]['price']} руб.\n {dishes[current_dish_index]['description']}", reply_markup=inline_keyboard)


def send_cart(chat_id):
    order = get_cart(chat_id)
    if not order[0]["dish_name"]:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    text = "Ваш заказ:\n"
    for dish in order:
        text += f"{dish['dish_name']} - {dish['quantity']} шт. - {dish['total']} руб.\n"
    text += f"\nОбщая стоимость: {sum([dish['total'] for dish in order])} руб."
    inline_keyboard = InlineKeyboardMarkup()
    btn_confirm = InlineKeyboardButton("Подтвердить заказ", callback_data="confirm_order")
    btn_back = InlineKeyboardButton("Назад", callback_data="category" + "|" + str(category_id))
    inline_keyboard.row(btn_confirm)
    inline_keyboard.row(btn_back)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

def send_payment_options(chat_id):
    order = get_cart(chat_id)
    if not order[0]["dish_name"]:
        bot.send_message(chat_id, "Ваша корзина пуста.")
        return
    text = "Ваш заказ:\n"
    for dish in order:
        text += f"{dish['dish_name']} - {dish['quantity']} шт. - {dish['total']} руб.\n"
    text += f"\nСумма к оплате: {sum([dish['total'] for dish in order])} руб."
    text += "\nВыберите способ оплаты:"
    change_order_status(chat_id, "confirmed")
    inline_keyboard = InlineKeyboardMarkup()
    btn_online = InlineKeyboardButton("Оплата онлайн", callback_data="pay_online")
    btn_cash = InlineKeyboardButton("Оплата наличными", callback_data="pay_cash")
    inline_keyboard.row(btn_online, btn_cash)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

def process_online_payment(chat_id, user_id):
    change_order_status(user_id, "paid")
    change_order_payment_method(user_id, "online")
    bot.send_message(chat_id, "Оплата прошла успешно! Ваш заказ оформлен.")
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=inline_keyboard)

def process_cash_payment(chat_id, user_id):
    change_order_status(user_id, "paid")
    change_order_payment_method(user_id, "cash")
    bot.send_message(chat_id, "Ваш заказ оформлен. Оплата наличными при получении.")
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, "Выберите действие:", reply_markup=inline_keyboard)

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
