from datetime import datetime

def print_function_name(func):
    def wrapper(*args, **kwargs):
        current_time = datetime.now()# Получаем текущее время
        formatted_time = current_time.strftime("%H:%M:%S") # Форматируем и выводим текущее время
        print(f"Функция {formatted_time}: ", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@print_function_name
def my_function():
    print("Выполняется функция.")

# my_function()