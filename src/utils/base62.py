ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
R_ALPHABET = {c: i for i, c in enumerate(ALPHABET)}
_BASE = len(ALPHABET)


def encode(base10_num: int) -> str:
    num = base10_num
    r = []
    while num > 0:
        num, rem = divmod(num, _BASE)
        r.append(ALPHABET[rem])
    r.reverse()
    return ''.join(r)


def decode(num: str) -> int:
    r = 0
    n = len(num)
    for i, c in enumerate(num):
        r += R_ALPHABET[c] * (_BASE ** (n - i - 1))
    return r
