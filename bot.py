# -*- coding: utf-8 -*-
import telebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
from base import *
from test import *
from datetime import datetime

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)


restaurants = get_restaurants()
dishes = {}

current_index = 0
current_dish_index = 0
category_id = None
completed_orders = {}
user_addresses = {}
user_orders_fb = {}
b_fb = False # для обработчика текстовых, что бы понимать что пришел отзыв
fb_num = -1  # номер заказа для отзыва в текстовом обработчике
fb_text = '' # текст отзыва в текстовом обработчике
fb_rate = 0 # оценка в текстовом обработчике
b_rate = False # для понимания, что в текстовом обработчике сейчас обрабатывается рейтнг


@print_function_name
@bot.message_handler(commands=['start'])
def send_welcome(message):
    #print(f'"/start" {message.chat.id}, {message.from_user.id}, {message.from_user.username}')

    add_user(message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name)
    username = message.from_user.first_name
    text = f"Привет, {username}! Я бот, который поможет тебе заказать еду."
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(message.chat.id, text, reply_markup=inline_keyboard)


@print_function_name
@bot.message_handler(func=lambda message: message.text == "Личный кабинет")
def profile_button_handler(message):
    send_user_profile(message.chat.id, message.from_user.id)

# Обработчик текстовых сообщений без каких-либо действий с БД, возвращаем на старт
@print_function_name
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    global b_fb, fb_num, user_orders_fb, b_rate, fb_text, fb_rate
    #print(f'{b_fb}, {fb_num}')

    user_text = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    #print(f'Обработчик текста. {user_id}, {username}, {user_text}')

    if (not b_rate) and b_fb:       # сюда попадаем после написания отзыва
        bot.send_message(message.chat.id, 'Спасибо! Мы обязательно передадим Ваш отзыв.\n А рейтинг (от 1 до 5)? Это обязательно!')
        fb_text = user_text
        b_rate = True
        return
    elif b_rate and b_fb:           # сюда попадаем после ввода рейтинга
        if not user_text.isdigit() or not 0 < int(user_text) < 6:
            bot.send_message(message.chat.id, 'Замечательная оценка!.\n Но нам нужны только цифры (от 1 до 5)! Попробуйте ещё раз.')
            return
        bot.send_message(message.chat.id, 'Замечательная оценка!.\n Спасибо!')
        fb_rate = user_text
        b_rate = False

    if b_fb:                        # отзыв пора передавать на запись в БД
        add_fb(message.chat.id, user_orders_fb[fb_num-1], fb_text, fb_rate,)  # Отправляем данные в БД [fb_num]
        b_fb = False                                          # Что бы не сохранять простой текст в БД
        b_rate = False
        send_welcome(message)                                   # Переходим в самое начало


@print_function_name
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    global current_index, current_dish_index, dishes, category_id, filename

    try:
        # Проверяем, что сообщение можно удалить
        if call.message.from_user.id == bot.get_me().id:  # Убедимся, что сообщение отправлено ботом
            bot.delete_message(call.message.chat.id, call.message.message_id)
    except telebot.apihelper.ApiTelegramException as e:
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"Не удалось удалить сообщение: {e}" + "\n")  # Добавляем информацию в конец файла
        print(f"Не удалось удалить сообщение: {e}")  # Логируем ошибку, но не прерываем выполнение

    if call.data.startswith("category"):
        category_id = int(call.data.split("|")[1])
        current_dish_index = 0
        dishes = get_dishes(category_id)
        send_category_info(call.message.chat.id)

    elif call.data.isdigit(): # отзыв на заказ
        #print(f'Отзыв на заказ {call.data}')
        ask_feedback(call.message.chat.id, call.from_user.id, call.data)

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
        add_to_cart(call.from_user.id, dishes[current_dish_index]["id"], dishes[current_dish_index]["price"], restaurants[current_index]["id"])
        send_category_info(call.message.chat.id)

    elif call.data == "cart":
        send_cart(call.message.chat.id)

    # elif call.data == "back_to_start":
    #     send_welcome(call.message)

    elif call.data == "back_to_start":
        send_welcome_directly(call.message.chat.id, call.from_user)


    elif call.data == "confirm_order":
        send_payment_options(call.message.chat.id)

    elif call.data == "pay_online":
        process_online_payment(call.message.chat.id, call.from_user.id)

    elif call.data == "profile":
        send_user_profile(call.message.chat.id, call.from_user.id)

    elif call.data == "order_history":
        send_user_orders(call.message.chat.id, call.from_user.id)

    elif call.data == "pay_cash":
        process_cash_payment(call.message.chat.id, call.from_user.id)

    elif call.data == "cancel_order":
        cancel_order(call.message.chat.id, call.from_user.id)

    elif call.data == "feedback":
        process_feedback(call.message.chat.id, call.from_user.id)

    elif call.data == "send_fb":
        echo_all(call.message)

    elif call.data == "add_adress":
        bot.send_message(call.message.chat.id, "Введите адрес доставки:")
        bot.register_next_step_handler(call.message, process_text)   # обработчик следующего сообщения от пользователя


@print_function_name
def process_text(message):
    user_text = message.text
    add_adress(message.chat.id, user_text)
    send_user_profile(message.chat.id, message.from_user.id)


@print_function_name
def add_adress(id, adress):
    print(f'Пользователь {id} адрес {adress}')
    add_user_adr(id, adress)


@print_function_name
def send_restaurant_info(chat_id):
    inline_keyboard = InlineKeyboardMarkup()
    btn_prev = InlineKeyboardButton("Пред.", callback_data="prev_restaurant")
    btn_next = InlineKeyboardButton("След.", callback_data="next_restaurant")
    btn_select = InlineKeyboardButton("Выбрать", callback_data="select_restaurant")
    btn_back = InlineKeyboardButton("Назад", callback_data="back_to_start")
    inline_keyboard.row(btn_prev, btn_next)
    inline_keyboard.row(btn_select)
    inline_keyboard.row(btn_back)
    ratings = get_rest_fb(restaurants[current_index]["id"])
    avg_rating = ratings[0]
    rating_count = ratings[1]
    text = f"Ресторан: {restaurants[current_index]['name']}\n" \
           f"Описание: {restaurants[current_index]['description']}\n" \
           f"Рейтинг: {avg_rating}  Отзывов: {rating_count}\n"
    image_path = restaurants[current_index]["logo"]
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        bot.send_photo(chat_id, photo=image_data, caption=text,
                       reply_markup=inline_keyboard)
    except Exception as e:
        print(f"Произошла ошибка: {e}")

@print_function_name
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


@print_function_name
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
    bot.send_message(chat_id, f"{dishes[current_dish_index]['name']} - {dishes[current_dish_index]['price']} руб.\n {dishes[current_dish_index]['description']}", reply_markup=inline_keyboard)

@print_function_name
def send_cart(chat_id):
    order = get_cart(chat_id)
    if not order:
        inline_keyboard = InlineKeyboardMarkup()
        btn_back = InlineKeyboardButton("Назад", callback_data="category" + "|" + str(category_id))
        inline_keyboard.row(btn_back)
        bot.send_message(chat_id, "Ваша корзина пуста.", reply_markup=inline_keyboard)
        return

    text = "Ваш заказ:\n"
    for dish in order:
        text += f"{dish['dish_name']} - {dish['quantity']} шт. - {dish['total']} руб.\n"
    text += f"\nОбщая стоимость: {sum([dish['total'] for dish in order])} руб."
    inline_keyboard = InlineKeyboardMarkup()
    btn_confirm = InlineKeyboardButton("Подтвердить заказ", callback_data="confirm_order")
    btn_cancel = InlineKeyboardButton("Отменить заказ", callback_data="cancel_order")
    btn_back = InlineKeyboardButton("Назад", callback_data="category" + "|" + str(category_id))
    inline_keyboard.row(btn_confirm)
    inline_keyboard.row(btn_cancel)
    inline_keyboard.row(btn_back)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

@print_function_name
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

@print_function_name
def process_online_payment(chat_id, user_id):
    order_id = get_current_order_id(user_id)
    change_order_status(user_id, "paid")
    change_order_payment_method(order_id, "online")
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, f"Оплата прошла успешно! Ваш заказ оформлен.\n Номер вашего заказа: {order_id}", reply_markup=inline_keyboard)

@print_function_name
def process_cash_payment(chat_id, user_id):
    order_id = get_current_order_id(user_id)
    change_order_status(user_id, "paid")
    change_order_payment_method(order_id, "cash")
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, f"Ваш заказ оформлен. Оплата наличными при получении.\n Номер вашего заказа: {order_id}", reply_markup=inline_keyboard)

@print_function_name
def send_user_profile(chat_id, user_id):
    adress = get_user_adr(user_id)
    username = get_username(user_id)[0]
    text = f"Имя пользователя: {username}\nАдрес доставки: {adress[0][0]}"
    inline_keyboard = InlineKeyboardMarkup()

    if adress[0][0] == None:
        btn_add_adr = InlineKeyboardButton("Добавить адрес доставки", callback_data="add_adress")
        inline_keyboard.row(btn_add_adr)
    else:
        btn_add_adr = InlineKeyboardButton("Изменить адрес доставки", callback_data="add_adress")
        inline_keyboard.row(btn_add_adr)

    btn_orders = InlineKeyboardButton("История заказов", callback_data="order_history")
    btn_fb = InlineKeyboardButton("Оставить отзыв", callback_data="feedback")
    btn_back = InlineKeyboardButton("Назад", callback_data="back_to_start")
    inline_keyboard.row(btn_orders)
    inline_keyboard.row(btn_fb)
    inline_keyboard.row(btn_back)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

@print_function_name
def send_user_orders(chat_id, user_id): # История заказов
    user_orders = get_user_orders(user_id)

    if not user_orders:
        inline_keyboard = InlineKeyboardMarkup()
        btn_profile = InlineKeyboardButton("Назад", callback_data="profile")
        inline_keyboard.add(btn_profile)
        bot.send_message(chat_id, "У вас нет заказов.", reply_markup=inline_keyboard)
    else:
        text = "Ваши заказы:\n"
        for order in user_orders:
            text += f"заказ от {order['updated_at']} - {order['status']} - {order['total_cost']} руб. - {order['payment_method']}\n"
        inline_keyboard = InlineKeyboardMarkup()
        btn_profile = InlineKeyboardButton("Назад", callback_data="profile")
        inline_keyboard.add(btn_profile)
        bot.send_message(chat_id, text, reply_markup=inline_keyboard)

@print_function_name
def process_feedback(chat_id, user_id): # Всё для отзыва
    global user_orders_fb
    buttons = [] # список кнопок
    row_butt = [] # список списков кнопок

    user_orders_fb = get_user_orders_fb(user_id)

    if not user_orders_fb:
        inline_keyboard = InlineKeyboardMarkup()
        btn_profile = InlineKeyboardButton("Назад", callback_data="profile")
        inline_keyboard.add(btn_profile)
        bot.send_message(chat_id, "У вас нет заказов.", reply_markup=inline_keyboard)
        return

    text = "Ваши заказы, на которые можно оставить отзыв:\n"
    num = 1
    for order in user_orders_fb:
        text += f"{num}. заказ от {order['updated_at']} - {order['status']} - {order['total_cost']} руб. - {order['payment_method']}\n"
        num += 1

    n = -1
    for i in range(num-1):  # создаём кнопки
        if i%6 == 0:
            row_butt.append([])
            n += 1
        row_butt[n].append(InlineKeyboardButton(text=str(i+1), callback_data=str(i+1)))

    inline_keyboard = InlineKeyboardMarkup(row_butt) # создаём кнопки на клавиатуре

    btn_profile = InlineKeyboardButton("Назад", callback_data="profile")
    inline_keyboard.add(btn_profile)
    text += "Выберете номер заказа для отзыва:"

    bot.send_message(chat_id, text, reply_markup=inline_keyboard)

@print_function_name
def ask_feedback(chat_id, user_id, num): # Отзыв получаем и отправляем БД
    global b_fb
    global fb_num
    fb_num = int(num)
    bot.send_message(chat_id, f'Напишите пару слов как Вам понравился или нет заказ №{num}:\n') #, reply_markup=inline_keyboard)
    b_fb = True # для обработчика текстовых что бы понимать что пришел отзыв

@print_function_name
def cancel_order(chat_id, user_id):
    change_order_status(user_id, "canceled")
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, "Ваш заказ отменен. Вы можете выбрать другой ресторан.", reply_markup=inline_keyboard)

@print_function_name
def send_welcome_directly(chat_id, user):
    add_user(chat_id, user.username, user.first_name, user.last_name)
    username = user.first_name
    text = f"Привет, {username}! Я бот, который поможет тебе заказать еду."
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(chat_id, text, reply_markup=inline_keyboard)


while True:
    try:
        global filename
        current_date = datetime.now().strftime("%Y-%m-%d") # Получаем текущую дату в формате ГГГГ-ММ-ДД
        filename = os.path.join(os.path.dirname(__file__), f"log_{current_date}.txt")  # Формируем имя файла


        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        time.sleep(10)  # Ожидание перед повторной попыткой

