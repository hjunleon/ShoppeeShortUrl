import random
import string


def random_string(n=10):
    return ''.join(random.choice(string.printable) for _ in range(n))
