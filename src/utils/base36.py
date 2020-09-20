ALPHABET = "ghijklmnopqrstuvwxyz"
R_ALPHABET = {c: i for i, c in enumerate(ALPHABET)}
_BASE = len(ALPHABET)


def encode(base10_num: int) -> str:
    num = base10_num
    r = []
    while num > 0:
        num, rem = divmod(num, _BASE)
        #r.insert(0,ALPHABET[rem])
        r.append(ALPHABET[rem])
    #r.reverse()
    return ''.join(r)


def decode(num: str) -> int:
    r = 0
    n = len(num)
    #print(n)
    idx = len(num)- 1
    while idx != -1:
        r += R_ALPHABET[num[idx]] * (_BASE ** (n - idx - 1))
        idx -= 1
    
    """
    for i, c in enumerate(num):
        r += R_ALPHABET[c] * (_BASE ** (n - i - 1))
        """
    return r