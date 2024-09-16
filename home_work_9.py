import os
import functools
from datetime import datetime


#ЗАДАНИЕ1
def logger(old_function):
    @functools.wraps(old_function)
    def new_function(*args, **kwargs):
        # Получаем текущее время
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Вызываем оригинальную функцию и получаем результат
        result = old_function(*args, **kwargs)

        # Формируем строку для записи в лог
        log_entry = (
            f"{current_time} - Function: {old_function.__name__}, "
            f"Args: {args}, Kwargs: {kwargs}, "
            f"Returned: {result}\n"
        )

        # Записываем лог в файл
        with open('main.log', 'a') as log_file:
            log_file.write(log_entry)

        return result

    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
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

    assert os.path.exists(path), 'файл main.log должен существовать'

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content, 'должно записаться имя функции'
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


#Задание2

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            # Подготовка информации для логирования
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            function_name = old_function.__name__
            arguments = args if args else kwargs
            result = old_function(*args, **kwargs)

            # Форматирование данных для записи
            log_entry = (
                f"{now} - Function '{function_name}' called with arguments {args} {kwargs}. "
                f"Returned: {result}\n"
            )

            # Запись в файл
            with open(path, 'a') as log_file:
                log_file.write(log_entry)

            return result

        return new_function

    return __logger

def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
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
    test_2()

