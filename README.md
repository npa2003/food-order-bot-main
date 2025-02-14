# food-order-bot
Исходнк (ветка main) создал Илья Гуляев.

# Внимание!
В проекте используется dotenv для сокрытия конфиденциальных данных, используемых в программе.
Для корректной работы необходимо установить dotenv - выполнить команду: "pip install python-dotenv".
Далее в корне проекта создаёте файл ".env".
В файле необходимо прописать строку: BOT_TOKEN = 'ВАШ bot_API_token'.
В таком случает токен будет храниться локально в Вашем проекте
___
### Бот для заказа еды
___
### Давайте подробно разберем предоставленный код, который создает Telegram-бота для заказа еды с использованием библиотеки `pyTelegramBotAPI`. Бот позволяет пользователям выбирать рестораны, просматривать меню, добавлять блюда в корзину и оформлять заказ.
___
**1. Импорт необходимых модулей:**

```python
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
```

- `telebot`: основная библиотека для работы с Telegram Bot API.
- `ReplyKeyboardMarkup`, `KeyboardButton`, `InlineKeyboardMarkup`, `InlineKeyboardButton`: классы из `telebot.types` для создания различных типов клавиатур и кнопок.
- `load_dotenv`: функция из библиотеки `python-dotenv` для загрузки переменных окружения из файла `.env`.
- `os`: стандартный модуль для работы с операционной системой, используется здесь для получения переменных окружения.
___
**2. Загрузка токена бота:**

```python
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)
```

- `load_dotenv()`: загружает переменные окружения из файла `.env`.
- `os.getenv("BOT_TOKEN")`: получает значение переменной окружения `BOT_TOKEN`, содержащей токен вашего бота.
- `telebot.TeleBot(TOKEN)`: создает экземпляр бота с указанным токеном.
___
**3. Определение данных:**

```python
restaurants = [
    {"name": "Ресторан №1", "logo": "https://static.tildacdn.com/tild3937-6436-4532-b065-313439633661/E9heAba_vzEory05dBFc.jpg"},
    {"name": "Ресторан №2", "logo": "https://teremok.ru/upload/iblock/947/sI2hxnNUDVM.jpg"},
]

soups = [
    {"name": "Борщ", "photo": "https://aif-s3.aif.ru/images/028/368/b4e33f182b30c9ce94fca1f35f4bd2a1.jpg", "price": 250},
    {"name": "Солянка", "photo": "https://ferma-alpatevo.ru/image/cache/catalog/2/soup/186-auto_width_1000.jpg", "price": 300}
]

current_index = 0
current_soup_index = 0
order = {"items": [], "total_price": 0}
```

- `restaurants`: список словарей с информацией о ресторанах, включая название и URL логотипа.
- `soups`: список словарей с информацией о супах, включая название, URL фотографии и цену.
- `current_index`: индекс текущего выбранного ресторана.
- `current_soup_index`: индекс текущего выбранного супа.
- `order`: словарь, представляющий текущий заказ пользователя, содержащий список выбранных блюд и общую сумму.
___
**4. Обработчик команды `/start`:**

```python
@bot.message_handler(commands=['start'])
def send_welcome(message):
    username = message.from_user.first_name
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    start_button = KeyboardButton("Старт")
    keyboard.add(start_button)
    bot.send_message(message.chat.id, "Нажмите 'Старт', чтобы начать", reply_markup=keyboard)
```

- Декоратор `@bot.message_handler(commands=['start'])` указывает, что функция `send_welcome` обрабатывает команду `/start`.
- Получает имя пользователя с помощью `message.from_user.first_name`.
- Создает клавиатуру с одной кнопкой "Старт" и отправляет сообщение с этой клавиатурой пользователю.
___
**5. Обработчик нажатия кнопки "Старт":**

```python
@bot.message_handler(func=lambda message: message.text == "Старт")
def handle_start(message):
    username = message.from_user.first_name
    text = f"Привет, {username}! Я бот, который поможет тебе заказать еду."
    inline_keyboard = InlineKeyboardMarkup()
    btn_restaurant = InlineKeyboardButton("Выбрать ресторан", callback_data="choose_restaurant")
    btn_profile = InlineKeyboardButton("Личный кабинет", callback_data="profile")
    inline_keyboard.add(btn_restaurant, btn_profile)
    bot.send_message(message.chat.id, text, reply_markup=inline_keyboard)
```

- Декоратор `@bot.message_handler(func=lambda message: message.text == "Старт")` указывает, что функция `handle_start` обрабатывает сообщения с текстом "Старт".
- Создает inline-клавиатуру с кнопками "Выбрать ресторан" и "Личный кабинет".
- Отправляет приветственное сообщение с этой клавиатурой.
___
**6. Обработчик нажатий inline-кнопок:**

```python
@bot.callback_query_handler(func=lambda call: True)
def handle_inline_buttons(call):
    global current_index, current_soup_index, order
    bot.delete_message(call.message.chat.id, call.message.message_id)

    if call.data == "choose_restaurant":
        current_index = 0
        send_restaurant_info(call.message.chat.id)
    elif call.data == "profile":
        bot.send_message(call.message.chat.id, "Личный кабинет в разработке.")
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
```
___
- Декоратор `@bot.callback_query_handler(func=lambda call: True)` указывает, что функция `handle_inline_buttons` обрабатывает все callback-запросы от inline-кнопок.
- В зависимости от значения `call.data` выполняются различные действия, такие как отображение информации о ресторане, меню, добавление супа в корзину и т.д.
- Используются вспомогательные функции `send_restaurant_info`, `send 
___



 
