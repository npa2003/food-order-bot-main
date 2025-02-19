def print_function_name(func):
    def wrapper(*args, **kwargs):
        print("Функция: ", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@print_function_name
def my_function():
    print("Выполняется функция.")

# my_function()