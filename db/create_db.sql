--1. Таблица users (Пользователи)
--Содержит информацию о пользователях Telegram.
--
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER NOT NULL UNIQUE,   -- идентификатор пользователя в Telegram
    username TEXT,                          -- имя пользователя (никнейм)
    first_name TEXT,
    last_name TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
--2. Таблица restaurants (Рестораны)
--Хранит данные о ресторанах, участвующих в системе.

-- restaurants definition

CREATE TABLE restaurants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    address TEXT,
    phone TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
, logo TEXT);

--3. Таблица categories (Категории блюд)
--Категории, к которым относятся блюда. Если меню ресторана разделено на категории (например, «Салаты», «Пицца», «Напитки»), то здесь хранятся эти разделы.

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    restaurant_id INTEGER NOT NULL,  -- категории могут быть специфичными для ресторана
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
--4. Таблица dishes (Блюда)
--Хранит информацию о блюдах меню.
CREATE TABLE dishes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    description TEXT,
    price REAL NOT NULL,
    image_url TEXT,                  -- URL изображения блюда (если требуется)
    category_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,  -- для удобства можно явно указывать ресторан (или выводить через category)
    available BOOLEAN DEFAULT 1,     -- флаг доступности блюда
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
--5. Таблица orders (Заказы)
--Содержит информацию о заказах, оформленных пользователями. Здесь можно использовать статус заказа для разделения «корзины» (пока заказ не подтверждён) и оформленных заказов.
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,      -- ресторан, в котором сделан заказ
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status TEXT NOT NULL,                -- например: 'cart', 'new', 'processing', 'completed', 'cancelled'
    total_cost REAL,                     -- итоговая стоимость (может рассчитываться при оформлении)
    payment_method TEXT,                 -- 'online' или 'cash'
    comment TEXT,                        -- комментарий к заказу (если требуется)
    updated_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id)
);
--6. Таблица order_items (Позиции заказа)
--Содержит список блюд, добавленных в заказ (или корзину) с указанием количества и цены на момент заказа.
CREATE TABLE order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    dish_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL,        -- цена за единицу блюда на момент заказа
    total REAL NOT NULL,        -- сумма = price * quantity
    note TEXT,                  -- дополнительные примечания (например, особые пожелания)
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
);
--7. Таблица reviews (Отзывы)
--Хранит отзывы, оставляемые пользователями. Отзыв может быть привязан как к конкретному заказу, так и напрямую к ресторану.
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    restaurant_id INTEGER NOT NULL,  -- отзыв для ресторана
    order_id INTEGER,                -- можно привязать к заказу (опционально)
    rating INTEGER NOT NULL,         -- оценка (например, от 1 до 5)
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
    FOREIGN KEY (order_id) REFERENCES orders(id)
);
--Обзор связей между таблицами
--Пользователь → Заказы: Каждый заказ (orders) привязан к пользователю (users).
--Ресторан → Категории → Блюда: Каждый ресторан может иметь несколько категорий (categories), а в каждой категории — несколько блюд (dishes).
--Заказ → Позиции заказа: Заказ состоит из нескольких записей в таблице order_items, где указывается, какие блюда и в каком количестве были выбраны.
--Пользователь/Ресторан → Отзывы: Пользователь может оставить отзыв для ресторана, возможно, с привязкой к конкретному заказу.
--Дополнительные замечания
--Статус заказа:
--Использование статуса (status) в таблице orders позволяет различать «корзину» (например, статус cart) и подтверждённые заказы (например, new, processing, completed и т.д.).
--
--Валидация данных:
--SQLite не накладывает строгие ограничения на типы, поэтому в логике приложения важно реализовать проверку корректности данных (например, чтобы rating находился в пределах от 1 до 5, quantity было положительным числом и т.п.).
--
--Расчёт итоговой суммы:
--Итоговая стоимость заказа (total_cost) может храниться в таблице orders для ускорения выборок, хотя её можно также вычислять динамически на основе данных из order_items.
--
--Расширяемость:
--При необходимости можно добавить таблицу для хранения истории платежей или дополнительную информацию о доставке.