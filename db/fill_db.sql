INSERT INTO users (telegram_id, username, first_name, last_name) VALUES
(123456789, 'john_doe', 'Иван', 'Иванов'),
(987654321, 'jane_doe', 'Мария', 'Петрова'),
(456789123, 'cool_user', 'Алексей', 'Смирнов'),
(654123987, 'happy_cat', 'Ольга', 'Кузнецова'),
(112233445, 'mystery_man', 'Дмитрий', 'Попов');

--Заполнение таблицы restaurants (3 ресторана)
INSERT INTO restaurants (name, description, address, phone) VALUES
('Итальянская кухня "Песто"', 'Лучшие блюда традиционной итальянской кухни.', 'г. Москва, ул. Тверская, д. 25', '+7 (495) 123-45-67'),
('Суши-бар "Сакура"', 'Свежие суши и роллы с доставкой.', 'г. Санкт-Петербург, Невский пр., д. 15', '+7 (812) 987-65-43'),
('Кафе "Домашний уголок"', 'Домашняя кухня для всей семьи.', 'г. Казань, ул. Баумана, д. 10', '+7 (843) 333-55-22');
--Заполнение таблицы categories (по 3–6 категорий на ресторан)
-- Для ресторана "Песто" (id 1)
INSERT INTO categories (name, description, restaurant_id) VALUES
('Пицца', 'Настоящая итальянская пицца.', 1),
('Паста', 'Традиционные итальянские макароны.', 1),
('Закуски', 'Лёгкие закуски к вашему столу.', 1),
('Десерты', 'Сладкие лакомства из Италии.', 1);

-- Для ресторана "Сакура" (id 2)
INSERT INTO categories (name, description, restaurant_id) VALUES
('Роллы', 'Роллы с начинками на любой вкус.', 2),
('Суши', 'Традиционные японские суши.', 2),
('Супы', 'Японские мисо и рамен.', 2),
('Напитки', 'Японский чай и другие напитки.', 2);

-- Для ресторана "Домашний уголок" (id 3)
INSERT INTO categories (name, description, restaurant_id) VALUES
('Супы', 'Горячие домашние супы.', 3),
('Горячие блюда', 'Традиционные кухня с домашним вкусом.', 3),
('Закуски', 'Лёгкие перекусы и салаты.', 3),
('Напитки', 'Чай, кофе и компоты.', 3),
('Десерты', 'Домашние сладости и выпечка.', 3);
--Заполнение таблицы dishes (200 блюд, распределённых между ресторанами и категориями)
--Вот несколько примеров, как можно заполнить записи для блюд (SQL-запросы реструктурированы для читаемости).

Блюда для ресторана "Песто" (пример 70 блюд)
-- Категория "Пицца" (id 1)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Маргарита', 'Классическая пицца с томатным соусом и сыром.', 450.00, 1, 1),
('Пепперони', 'Острая пицца с пепперони и сыром.', 500.00, 1, 1),
('Четыре сыра', 'Пицца с голубым сыром, моцареллой, пармезаном и горгондзолой.', 550.00, 1, 1);

-- Категория "Паста" (id 2)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Карбонара', 'Паста с беконом в сливочном соусе.', 400.00, 2, 1),
('Болоньезе', 'Паста с мясным соусом болоньезе.', 420.00, 2, 1),
('Лазанья', 'Итальянская лазанья с мясной начинкой.', 600.00, 2, 1);

-- Категория "Закуски" (id 3)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Брускетта с помидорами', 'Обжаренный хлеб с томатами и базиликом.', 300.00, 3, 1),
('Оливки', 'Солёные оливки с пряностями.', 250.00, 3, 1);

-- Категория "Десерты" (id 4)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Тирамису', 'Традиционный итальянский десерт.', 280.00, 4, 1),
('Канноли', 'Сицилийская трубочка с рикоттой.', 320.00, 4, 1);
--Блюда для ресторана "Сакура" (пример 70 блюд)
-- Категория "Роллы" (id 5)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Калифорния', 'Ролл с крабовым мясом и авокадо.', 500.00, 5, 2),
('Филадельфия', 'Ролл с красной рыбой и сливочным сыром.', 550.00, 5, 2);

-- Категория "Суши" (id 6)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Суши с лососем', 'Суши с филе свежего лосося.', 150.00, 6, 2),
('Суши с тунцом', 'Суши с тунцом.', 180.00, 6, 2);

-- Категория "Супы" (id 7)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Рамен', 'Японский суп с лапшой и мясом.', 400.00, 7, 2),
('Мисо', 'Классический японский суп с тофу и вакамэ.', 350.00, 7, 2);
--Блюда для ресторана "Домашний уголок" (пример 60 блюд)
-- Категория "Супы" (id 8)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Борщ', 'Традиционный борщ со сметаной.', 250.00, 8, 3),
('Рассольник', 'Горячий рассольник с перловкой.', 230.00, 8, 3);

-- Категория "Десерты" (id 9)
INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Шарлотка', 'Классическая шарлотка с яблоками.', 200.00, 9, 3),
('Медовик', 'Домашний торт с медом.', 220.00, 9, 3);

INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Гавайская', 'Пицца с курицей, ананасами и сыром.', 480.00, 1, 1),
('Диабло', 'Острая пицца с пепперони, халапеньо и перцем чили.', 520.00, 1, 1),
('Мясная', 'Пицца с разными видами мяса и сыром.', 600.00, 1, 1),
('Капричоза', 'Томатный соус, ветчина, грибы и артишоки.', 550.00, 1, 1),
('Маринара', 'Томатный соус, чеснок, орегано.', 450.00, 1, 1),
('Овощная', 'Пицца с ассорти из свежих овощей.', 430.00, 1, 1),
('Моцарелла', 'Пицца со свежей моцареллой и базиликом.', 470.00, 1, 1),
('Тартуфо', 'Пицца с трюфельным маслом и сыром.', 650.00, 1, 1),
('Дьябло-Бекон', 'Комбинация бекона, острого соуса и перцев.', 590.00, 1, 1),
('Пицца с морепродуктами', 'Креветки, кальмары, мидии и белое вино.', 750.00, 1, 1);

INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Паста с грибами', 'Домашняя паста с шампиньонами в сливочном соусе.', 480.00, 2, 1),
('Пенне с вялеными томатами', 'Классическая паста с нежным соусом.', 520.00, 2, 1),
('Фетучини Альфредо', 'Паста с курицей в сливочном соусе.', 490.00, 2, 1),
('Паста с морепродуктами', 'Креветки, кальмары в белом соусе.', 580.00, 2, 1),
('Орекьетте с беконом', 'Итальянская паста с беконом и травами.', 460.00, 2, 1),
('Спагетти с томатным соусом', 'Простая и вкусная паста.', 430.00, 2, 1),
('Тальятелле Болоньезе', 'Классический соус болоньезе с пастой.', 500.00, 2, 1),
('Гнокки с сырным соусом', 'Картофельные клецки в сливочном сырном соусе.', 470.00, 2, 1),
('Паста с чернилами каракатицы', 'Оригинальная паста с насыщенным вкусом.', 610.00, 2, 1),
('Ригатони с соусом из шпината', 'Паста с соусом из свежего шпината.', 450.00, 2, 1);

INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Кепресе', 'Свежие томаты, моцарелла и базилик.', 300.00, 3, 1),
('Овощной антре', 'Ассорти из свежих овощей с соусом.', 320.00, 3, 1),
('Гарлик Брэд', 'Обжаренные чесночные булочки.', 200.00, 3, 1),
('Фокачча', 'Итальянский хлеб с оливковым маслом.', 240.00, 3, 1),
('Артишоки', 'Жареные артишоки в масле.', 400.00, 3, 1),
('Оливки с сыром', 'Оливки, фаршированные сыром.', 250.00, 3, 1),
('Тартар из тунца', 'Свежий тунец с соусом на крекере.', 550.00, 3, 1),
('Карпаччо из говядины', 'Тонкие ломтики говядины с лимоном.', 580.00, 3, 1),
('Крудо', 'Ассорти из свежих рыбы и овощей.', 600.00, 3, 1),
('Крокеты с сыром', 'Жареные крокеты со сливочным сыром.', 290.00, 3, 1);

INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Панна Котта', 'Десерт на основе сливок с ягодным соусом.', 330.00, 4, 1),
('Шоколадный фондан', 'Тёплый десерт с растопленным шоколадом.', 370.00, 4, 1),
('Джелато', 'Классическое итальянское мороженое.', 300.00, 4, 1),
('Сицилийские канноли', 'Хрустящие трубочки с кремом.', 400.00, 4, 1),
('Чизкейк с лимоном', 'Итальянская версия чиза.', 380.00, 4, 1),
('Сабайон', 'Воздушный крем с вином Марсала.', 420.00, 4, 1),
('Кростата с инжиром', 'Пирог из песочного теста.', 450.00, 4, 1),
('Торт из рикотты', 'Плотный, но сладкий.', 410.00, 4, 1);

INSERT INTO dishes (name, description, price, category_id, restaurant_id) VALUES
('Суши с тунцом', 'Свежий тунец на рисовом основании.', 180.00, 6, 2),
('Суши с лососем', 'Лосось на подушке из риса.', 190.00, 6, 2),
('Суши с угрём', 'Копчёный угорь с соусом унаги.', 200.00, 6, 2),
('Суши с креветкой', 'Креветка на подушке из ароматного риса.', 170.00, 6, 2),
('Суши с гребешком', 'Нежный японский гребешок на рисе.', 220.00, 6, 2),
('Суши с окунем', 'Свежий окунь с лёгким лимонным акцентом.', 180.00, 6, 2),
('Суши с крабовым мясом', 'Нежное крабовое мясо с рисом.', 200.00, 6, 2),
('Суши с омлетом Тамаго', 'Японский сладковатый омлет.', 150.00, 6, 2),
('Суши с осьминогом', 'Свежий осьминог с васаби.', 210.00, 6, 2),
('Суши с красной икрой', 'Икра кеты на рисовой основе.', 250.00, 6, 2),
('Суши с кальмаром', 'Ломтики свежего кальмара на рисе.', 190.00, 6, 2),
('Суши с остролистом', 'Экзотический вид рыбы для гурманов.', 230.00, 6, 2),
('Суши с икрой летучей рыбы', 'Яркая икра тобико.', 160.00, 6, 2),
('Суши с морским ежом', 'Нежный морской ёж на рисе.', 300.00, 6, 2),
('Суши с копчёным лососем', 'Лосось подкопчённый, с рисом.', 240.00, 6, 2),
('Суши с фугу', 'Экзотическая рыба-фугу. Приготовлено мастером.', 450.00, 6, 2),
('Суши с белым тунцом', 'Элегантный вкус белого тунца.', 210.00, 6, 2),
('Суши с авокадо', 'Освежающая вегетарианская опция.', 140.00, 6, 2),
('Суши с огурцом', 'Простое и полезное сочетание.', 130.00, 6, 2),
('Суши с сливочным сыром', 'Рисовое основание с мягким сыром.', 150.00, 6, 2),
('Суши с тунцом и авокадо', 'Комбинация тунца и авокадо.', 220.00, 6, 2),
('Суши с крабом и манго', 'Яркое сочетание краба и манго.', 270.00, 6, 2),
('Суши с вяленым лососем', 'Лосось, выдержанный в соли и травах.', 230.00, 6, 2),
('Суши с угрём и авокадо', 'Традиционный угорь с авокадо.', 260.00, 6, 2),
('Суши с копчёной уткой', 'Необычное, но оригинальное блюдо.', 300.00, 6, 2),
('Суши с сливочным лососем', 'Лосось с добавлением сливок.', 240.00, 6, 2),
('Суши с мидиями', 'Рискованно вкусные мидии.', 190.00, 6, 2),
('Суши с гребешками и лимоном', 'Свежие гребешки с цитрусовым оттенком.', 260.00, 6, 2),
('Суши с копчёным осьминогом', 'Подкопчённый осьминог.', 240.00, 6, 2),
('Суши с горчичной икрой', 'Пикантное сочетание.', 180.00, 6, 2),
('Суши с трюфельным маслом', 'Яркий вкус трюфеля.', 280.00, 6, 2),
('Суши с баклажаном', 'Вегетарианский вариант.', 150.00, 6, 2),
('Суши с лососем и лимоном', 'Лосось на рисе с цитрусовой нотой.', 200.00, 6, 2),
('Суши с базиликом и тунцом', 'Свежий тунец с ароматной зеленью.', 220.00, 6, 2),
('Суши с угрём и трюфелем', 'Премиальное сочетание угря и трюфеля.', 350.00, 6, 2),
('Суши с сыром и васаби', 'Необычная, но простая подача.', 200.00, 6, 2),
('Суши с крабом и трюфелем', 'Нежное сочетание краба и трюфеля.', 340.00, 6, 2),
('Суши с тунцом и огурцом', 'Свежий тунец содержит баланс.', 180.00, 6, 2),
('Суши с тигровой креветкой', 'Сочная тигровая креветка.', 300.00, 6, 2),
('Суши с белым осьминогом', 'Основа из белоснежного осьминога.', 260.00, 6, 2);


delete from dishes where id in (
select min(id) from dishes d group by name,category_id having count(*)>1 
);

select  r.name,c.name,count(*)  from restaurants r 
 join categories c  on c.restaurant_id= r.id
 join dishes d on d.category_id = c.id 
group by r.name,c.name
order by 2


 orders definition
INSERT INTO orders (user_id, restaurant_id, status, total_cost, payment_method, comment, updated_at) VALUES
(1, 1, 'completed', 1250.00, 'online', 'Первый заказ, пицца и паста.', DATETIME('now')),
(1, 1, 'completed', 890.00, 'cash', 'Взял пасту и несколько роллов.', DATETIME('now')),
(1, 2, 'completed', 920.00, 'online', 'Попробовал суши с новой начинкой.', DATETIME('now')),
(1, 3, 'completed', 670.00, 'cash', 'Просто закуски с напитком.', DATETIME('now')),
(1, 1, 'completed', 2300.00, 'online', 'Для празднования дня рождения — пиццы, пасты, суши.', DATETIME('now')),
(1, 2, 'cancelled', 1350.00, 'cash', 'По ошибке заказал не в тот день.', DATETIME('now')),
(1, 3, 'completed', 780.00, 'online', 'Лёгкие десерты и кофе.', DATETIME('now')),
(1, 2, 'cart', 450.00, 'online', NULL, DATETIME('now')), -- Заказ в корзине
(1, 1, 'processing', 1800.00, 'cash', 'Ожидаю приготовления заказа.', DATETIME('now')),
(1, 2, 'processing', 640.00, 'online', 'Захотелось чего-то нового.', DATETIME('now'));

-- Заказы от второго пользователя (user_id = 2)
INSERT INTO orders (user_id, restaurant_id, status, total_cost, payment_method, comment, updated_at) VALUES
(2, 2, 'completed', 950.00, 'online', 'Восхитительные суши для ужина.', DATETIME('now')),
(2, 1, 'completed', 670.00, 'cash', 'Пицца для семьи.', DATETIME('now')),
(2, 3, 'new', 450.00, 'online', 'Закуски для перекуса в офисе.', DATETIME('now'));

-- Заказ от третьего пользователя (user_id = 3)
INSERT INTO orders (user_id, restaurant_id, status, total_cost, payment_method, comment, updated_at) VALUES
(3, 2, 'completed', 760.00, 'cash', 'Попробовал сет с суши.', DATETIME('now'));

-- Заказ 1 (user_id = 1, order_id = 1)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(1, 1, 2, 480.00, 960.00, 'Пицца Гавайская (2 штуки)'),
(1, 14, 1, 290.00, 290.00, 'Паста с грибами');

-- Заказ 2 (user_id = 1, order_id = 2)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(2, 2, 1, 520.00, 520.00, NULL), -- Пицца Диабло
(2, 48, 2, 180.00, 360.00, 'Суши с тунцом (2 порции)');

-- Заказ 3 (user_id = 1, order_id = 3)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(3, 47, 1, 190.00, 190.00, NULL), -- Суши с лососем
(3, 50, 2, 170.00, 340.00, 'Суши с креветкой');

-- Заказ 4 (user_id = 1, order_id = 4)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(4, 3, 1, 600.00, 600.00, NULL), -- Пицца Мясная
(4, 16, 1, 490.00, 490.00, 'Паста Альфредо');

-- Заказ 5 (user_id = 1, order_id = 5)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(5, 1, 1, 480.00, 480.00, NULL), -- Пицца Гавайская
(5, 47, 1, 190.00, 190.00, 'Суши с лососем'),
(5, 2, 2, 520.00, 1040.00, 'Пицца Диабло, 2 шт.');

-- Заказ 6 (user_id = 1, order_id = 6)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(6, 50, 1, 170.00, 170.00, 'Суши с креветкой'),
(6, 3, 2, 600.00, 1200.00, 'Пицца Мясная, двойное количество');

-- Заказ 7 (user_id = 1, order_id = 7)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(7, 33, 3, 160.00, 480.00, 'Роллы тобико с икрой, 3 шт.'),
(7, 16, 1, 470.00, 470.00, 'Паста с сырным соусом');

-- Заказ 8 (user_id = 1, order_id = 8)
-- Пустая корзина или сохранённый заказ; обновить позже.

-- Заказ 9 (user_id = 1, order_id = 9)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(9, 3, 1, 600.00, 600.00, 'Пицца Мясная'),
(9, 48, 1, 180.00, 180.00, 'Суши с тунцом');

-- Заказ 10 (user_id = 1, order_id = 10)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(10, 42, 2, 230.00, 460.00, 'Суши с угрём и авокадо');
Заказы от второго пользователя:
-- Заказ 11 (user_id = 2, order_id = 11)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(11, 47, 2, 190.00, 380.00, 'Суши с лососем, двойная порция'),
(11, 50, 2, 170.00, 340.00, NULL); -- Суши с креветкой

-- Заказ 12 (user_id = 2, order_id = 12)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(12, 1, 1, 480.00, 480.00, 'Пицца Гавайская');

-- Заказ 13 (user_id = 2, order_id = 13)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(13, 33, 3, 160.00, 480.00, 'Тобико роллы, 3 упаковки.');
Заказ от третьего пользователя:
-- Заказ 14 (user_id = 3, order_id = 14)
INSERT INTO order_items (order_id, dish_id, quantity, price, total, note) VALUES
(14, 49, 3, 250.00, 750.00, 'Суши с красной икрой, потрясающе.');


-- Три отзыва от первого пользователя (user_id = 1)
INSERT INTO reviews (user_id, restaurant_id, order_id, rating, comment, created_at) VALUES
-- Отзыв на заказ 1 из ресторана 1
(1, 1, 1, 5, 'Пицца и паста были на высшем уровне, горячее и свежее!', DATETIME('now')),
-- Отзыв на заказ 3 из ресторана 2
(1, 2, 3, 4, 'Суши с лососем немного пресные, но креветки понравились.', DATETIME('now')),
-- Отзыв на заказ 7 из ресторана 3
(1, 3, 7, 5, 'Десерты вкусные, персонал вежливый. Вернусь еще.', DATETIME('now'));

-- Один отзыв от второго пользователя (user_id = 2)
INSERT INTO reviews (user_id, restaurant_id, order_id, rating, comment, created_at) VALUES
-- Отзыв на заказ 11 из ресторана 2
(2, 2, 11, 5, 'Суши были свежими и вкусными, доставка быстрая. Рекомендую!', DATETIME('now'));

- Негативный отзыв 1 от пользователя 1 (низкая оценка на заказ из ресторана 2)
INSERT INTO reviews (user_id, restaurant_id, order_id, rating, comment, created_at) VALUES
(1, 2, 6, 1, 'Еда приехала холодной, суши были сухими. Очень разочарован.', DATETIME('now'));

-- Негативный отзыв 2 от пользователя 1 (низкая оценка на заказ из ресторана 1)
INSERT INTO reviews (user_id, restaurant_id, order_id, rating, comment, created_at) VALUES
(1, 1, 9, 2, 'Пицца не соответствует заявленному составу, ингредиенты среднего качества.', DATETIME('now'));

-- Дополнительно : заполнение лого
update restaurants set logo= 'https://assets.turbologo.ru/blog/ru/2019/05/18163916/SAKURA.png' where id = 2;
update restaurants set name='Fatboys', logo= 'data:image/png;base64,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' where id = 1;
update restaurants set logo= 'data:image/jpeg;base64,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' where id =3;
