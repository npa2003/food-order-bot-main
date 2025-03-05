# -*- coding: utf-8 -*-
from datetime import datetime

filename = ''

def print_function_name(func):
    def wrapper(*args, **kwargs):
        global filename
        current_time = datetime.now()# Получаем текущее время
        formatted_time = current_time.strftime("%d-%m-%y | %H:%M:%S") # Форматируем и выводим текущее время
        current_date = datetime.now().strftime("%Y-%m-%d") # Получаем текущую дату в формате ГГГГ-ММ-ДД
        text = f'[{formatted_time}] {func.__name__} {args} {kwargs}' # строка для записи и печати
        filename = f"log_{current_date}.txt" # Формируем имя файла

        # Записываем информацию в файл. Если файла нет, то он создаётся
        with open(filename, "a", encoding="utf-8") as file:
            file.write(text + "\n")  # Добавляем информацию в конец файла

        print(text)
        return func(*args, **kwargs)
    return wrapper

# my_function()