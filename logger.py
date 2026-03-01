import os
from datetime import datetime


# === Задание 1: Простой декоратор logger (записывает в main.log) ===
def logger(old_function):
    def new_function(*args, **kwargs):
        result = old_function(*args, **kwargs)
        with open('main.log', 'a', encoding='utf-8') as f:
            log_entry = f'{datetime.now()} - {old_function.__name__}({args}, {kwargs}) -> {result}\n'
            f.write(log_entry)
        return result
    return new_function


# === Задание 2: Параметризованный декоратор logger_with_path ===
def logger_with_path(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            result = old_function(*args, **kwargs)
            with open(path, 'a', encoding='utf-8') as f:
                log_entry = f'{datetime.now()} - {old_function.__name__}({args}, {kwargs}) -> {result}\n'
                f.write(log_entry)
            return result
        return new_function
    return __logger


# === Тест 1: использует простой logger ===
def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger  # ← должен быть простой logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
    result = summator(2, 2)
    assert isinstance(result, int), 'Должно вернуться целое число'
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'
    summator(4.3, b=2.2)

    assert os.path.exists(path), 'файл main.log должен существовать'

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


# === Тест 2: использует параметризованный logger_with_path ===
def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger_with_path(path)  # ← теперь всё правильно
        def hello_world():
            return 'Hello World'

        @logger_with_path(path)
        def summator(a, b=0):
            return a + b

        @logger_with_path(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b=2.2)

    for path in paths:
        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'
        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()
    test_2()
    print("✅ Все тесты пройдены!")