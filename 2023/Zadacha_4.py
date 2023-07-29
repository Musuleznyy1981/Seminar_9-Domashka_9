# Мусулезный Максим ,задача №4
# Создайте декоратор с параметром. Параметр - целое число, количество запусков декорируемой функции.
from typing import Callable


def counter(param: int):
    def deco_c(func: Callable):
        my_list = []

        def wrapper(*args, **kwargs):
            for i in range(param):
                result = func(*args, **kwargs)
                my_list.append(result)
            return my_list

        return wrapper

    return deco_c


@counter(3)
def fact(num: int) -> int:
    res = 1
    for i in range(1, num + 1):
        res *= i
    return res


if __name__ == '__main__':
    print(fact(4))

    # Вариант 2
    def counter(n: int):
        lst_counter = []

        def deco(func: callable):
            def wrapper(*args, **kwargs):
                for _ in range(n):
                    lst_counter.append(func(*args, **kwargs))
                return lst_counter

            return wrapper

        return deco


    @counter(11)
    def test(*args, **kwargs) -> int:
        return sum(args)


    print(test(111, 222, 333))