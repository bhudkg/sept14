import string

BASE62 = string.digits + string.ascii_letters


def encode(num: int) -> str:
    '''Function to encode a int into base62'''
    try:
        if num == 0:
            return BASE62[0]

        res = []
        while num > 0:
            res.append(BASE62[num%62])
            num//=62
        return "".join(reversed(res))

    except Exception as e:
        print(e)

# print(encode(611))

def decode(code: str):
    '''Function to decode base62 string in int'''
    try:
        num = 0
        for c in code:
            num = num*62 + BASE62.index(c)
        return num

    except Exception as e:
        print(e)
    

print(decode(encode(611)))

