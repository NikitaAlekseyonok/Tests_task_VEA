import time
from random import choice
from string import ascii_letters


def set_random_string():
    random_string = (''.join(choice(ascii_letters) for i in range(7)))
    return random_string


def set_test_status(test_status):
    if test_status == 'In progress':
        return test_status
    else:
        return test_status.upper()
