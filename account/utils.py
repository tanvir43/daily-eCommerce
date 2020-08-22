import random
from random import randint


def random_unique_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    choices = list(range(range_start, range_end))
    random.shuffle(choices)
    return choices.pop()


def random_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)