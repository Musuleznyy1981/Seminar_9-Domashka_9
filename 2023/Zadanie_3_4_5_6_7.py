# Мусулезный Максим , задания №3,4,5,6,7
# Решить задачи, которые не успели решить на семинаре.
# Напишите следующие функции:
# Нахождение корней квадратного уравнения
# Генерация csv файла с тремя случайными числами в каждой строке.100-1000 строк.
# Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
# Декоратор, сохраняющий переданные параметры и результаты работы  функции в json файл.
# Соберите пакет с играми из тех файлов, что уже были созданы в рамках курса


# 1 ВАРИАНТ
import csv
import json
import random
import math
import functools

# Нахождение корней квадратного уравнения
def find_roots(a, b, c):
    discriminant = b**2 - 4*a*c
    if discriminant >= 0:
        x1 = (-b + math.sqrt(discriminant)) / (2*a)
        x2 = (-b - math.sqrt(discriminant)) / (2*a)
        return (x1, x2)
    else:
        return ("Complex roots",)

# Генерация csv файла с тремя случайными числами в каждой строке. 100-1000 строк.
def generate_csv(filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        for _ in range(random.randint(100, 1001)):
            writer.writerow([random.randint(0,100) for _ in range(3)])

# Декоратор, запускающий функцию нахождения корней квадратного уравнения с каждой тройкой чисел из csv файла.
def from_csv_decorator(func):
    @functools.wraps(func)
    def wrapper(filename):
        results = []
        with open(filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                a, b, c = map(int, row)
                results.append(func(a, b, c))
        return results
    return wrapper

# Декоратор, сохраняющий переданные параметры и результаты работы функции в json файл.
def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        with open('log.json', 'a') as f:
            json.dump({'func': func.__name__, 'args': args, 'kwargs': kwargs, 'result': result}, f)
        return result
    return wrapper


# 2 ВАРИАНТ
import csv
import json
import random
from cmath import sqrt
from typing import Callable


def find_root_in_csv_deco(func: Callable) -> object:
    def wrapper(*args, **kwargs):
        equations = {}
        with open('odds.csv', 'r') as f:
            reader = csv.reader(f, dialect='excel')
            count = 0
            equation = {}
            for row in reader:
                if count > 0:
                    equation = {count: {'a': int(row[0]),
                                        'b': int(row[1]),
                                        'c': int(row[2]),
                                        'result': func(int(row[0]), int(row[1]), int(row[2]))}}
                equations.update(equation)
                count += 1
        return equations

    return wrapper


def write_json(func: Callable):
    def wrapper(*args, **kwargs):
        result = func()
        print(result)
        with open('odds.json', 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

    return wrapper


@write_json
@find_root_in_csv_deco
def find_root(a: int = 1, b: int = 1, c: int = 1) -> tuple[str, str] | str:
    discriminant = (pow(b, 2)) - (4 * a * c)
    if discriminant < 0:
        return f'нет действительных корней'
    if discriminant == 0:
        return str(-b / (2 * a))
    else:
        if a != 0:
            return str((-b + sqrt(discriminant)) / (2 * a)), str((-b - sqrt(discriminant)) / (2 * a))


def generate_numbers() -> int:
    MIN_NUM = 1
    MAX_NUM = 9
    MIN_LEN = 1
    MAX_LEN = 5
    generated_num = ''
    rnd_len = random.randint(MIN_LEN, MAX_LEN)
    for _ in range(1, rnd_len + 1):
        generated_num += str(random.randint(MIN_NUM, MAX_NUM))
    return int(generated_num)


def make_line() -> str:
    COUNT_NUMS = 3
    for i in range(COUNT_NUMS):
        yield str(generate_numbers())


def write_csv(file: str) -> None:
    LINE_COUNT = 100
    list_csv = []
    for _ in range(LINE_COUNT):
        num_1, num_2, num_3 = make_line()
        list_csv.append([num_1, num_2, num_3])
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['a', 'b', 'c'])
        writer.writerows(list_csv)



if __name__ == '__main__':
    write_csv('odds.csv')
    find_root()