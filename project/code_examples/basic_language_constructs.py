from .basic import *

# __iter__
_sum = 0
for el in arr:
    _sum += el

# __callable__
def basic_func(a, b, *args, **kwargs):
    c = a + b
    return (c, c ** 2, c ** 3)


res = basic_func(a, b)


# first class functions
def closure():
    def child_func():
        return 1

    return child_func


_func = closure()

# comprehensions
comp = [i for i in range(100) if i % 2 == 0]
# generators
gen = next(i for i in range(100) if i % 9 == 0)
