import os
import datetime
from functools import wraps

def logger(path):
    def _logger(old_function):
        @wraps(old_function)
        def new_function(*args, **kwargs):
            now = datetime.datetime.now()
            log = ''
            log += f"{'Время вызова функции: ' + str(now):=^100}\n"
            result = old_function(*args, **kwargs)
            log += f'Имя вызванной функции: {old_function.__name__}\n'
            log += f'Аргументы вызванной функции: {args} и {kwargs}\n'
            log += f'Значение, возвращаемое функцией: {result}\n'
            os.chdir(os.path.dirname(os.path.abspath(__file__)))  # This may not be necessary depending on your use case
            with open(path, 'a+', encoding='utf-8') as f:
                f.write(log)
            return result

        return new_function

    return _logger

def test_3():
    paths = ('log_foo_1.log',)
    for path in paths:
        if os.path.exists(path):
            os.remove(path)

        @logger(path)
        def call(weekday, days):
            weekdays_dict = {
                'Monday': 1,
                'Tuesday': 0,
                'Wednesday': -1,
                'Thursday': -2,
                'Friday': -3,
                'Saturday': -4,
                'Sunday': -5
            }
            start = weekdays_dict.get(weekday, 0)  # Default to 0 if weekday is not found

            out = []
            for k in range(start, days + 1):
                if k <= 0:
                    out.append('..')
                elif 0 < k < 10:
                    out.append(f'.{k}')
                else:
                    out.append(k)
                if (k - start + 1) % 7 == 0:  # Changed to accommodate the actual position
                    out.append('\n')

            return out

        calendar = call('Thursday', 30)
        print(*calendar)

if __name__ == '__main__':
    test_3()
