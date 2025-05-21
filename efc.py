#! python3
# coding: utf-8

# Enhanced Fibonacci Coding

def _feb3_next(c1, c2):
    return c1 + c2

def _feb3_prev(c1, c2):
    return c2 - c1

def _buf_push_int(buf, b):
    return (buf << 1) | b

_buf_push = _buf_push_int

def _feb_adic_enc(src, buf):
    c1 = 1
    c2 = 1
    while True:
        v = _feb3_next(c1, c2)
        if v > src:
            break
        c1 = c2
        c2 = v
    buf = _buf_push(buf, 1)
    cur = src - c2
    while c2 > 1:
        if cur >= c1:
            buf = _buf_push(buf, 1)
            cur -= c1
        else:
            buf = _buf_push(buf, 0)
        v = _feb3_prev(c1, c2)
        c2 = c1
        c1 = v
    assert cur == 0
    return buf

if __name__ == '__main__':
    import pdb
    from hexdump import hexdump as hd
    from pprint import pprint
    ppr = lambda *a, **ka: pprint(*a, **ka, sort_dicts = False)
