# Задача №5
# Объедините функции из прошлых задач.
# Функцию угадайку задекорируйте декораторами для
# сохранения параметров, декоратором контроля значений
# и декоратором для многократного запуска.
# Выберите верный порядок декораторов.
import json
from random import randint
from functools import wraps

LOVER_LIMIT_TRIES = 1
UPPER_LIMIT_TRIES = 10
LOVER_LIMIT_NUM = 1
UPPER_LIMIT_NUM = 100


def game_decorator(func: callable) -> callable:

    @wraps(func)
    def wrapper(num: int, count: int, *args, **kwargs) -> bool:
        if num < LOVER_LIMIT_NUM or num > UPPER_LIMIT_NUM:
            num = randint(LOVER_LIMIT_NUM, UPPER_LIMIT_NUM)
        if count < LOVER_LIMIT_TRIES or count > UPPER_LIMIT_TRIES:
            count = randint(LOVER_LIMIT_TRIES, UPPER_LIMIT_TRIES)
        return func(num, count)
    return wrapper


def counter(n: int):
    lst_counter = []

    def deco(func: callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                lst_counter.append(func(*args, **kwargs))
            return lst_counter
        return wrapper
    return deco


def json_cache(func: callable) -> callable:
    try:
        with open(f"{func.__name__}.json", 'r') as log:
            data = json.load(log)
    except FileNotFoundError:
        with open(f"{func.__name__}.json", 'w') as log:
            data = []
            json.dump(data, log, indent=4)

    @wraps(func)
    def wrapper(*args, **kwargs) -> None:
        temp_dict = {'args': args, 'kwargs': kwargs, 'result': func(*args, **kwargs)}
        data.append(temp_dict)
        with open(f"{func.__name__}.json", 'w') as log:
            json.dump(data, log, indent=4)

    return wrapper


@counter(3)
@json_cache
@game_decorator
def game_w_dec(num: int, count: int) -> bool:
    for _ in range(count):
        user_number = int(input('Введите число: '))
        if user_number == num:
            print('Угадали')
            return True
        elif user_number < num:
            print('Число больше')
        else:
            print('Число меньше')
    print('Попытки кончились')
    return False


game_w_dec(200, 97)