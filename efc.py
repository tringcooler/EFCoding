#! python3
# coding: utf-8

# Enhanced Fibonacci Coding

def _feb3_next(c1, c2):
    return c2, c1 + c2

def _feb3_prev(c1, c2):
    return c2 - c1, c1

def _buf_push_int(buf, blen, v, n):
    return (buf << n) | v, blen + n

def _buf_push_any_int(buf, blen, n):
    return buf << n, blen + n

def _buf_set_int(buf, v, n):
    return buf | (v << n)

def _buf_pop_int(buf, blen):
    return buf, blen - 1, (buf >> (blen - 1)) & 1

_buf_push = _buf_push_int
_buf_push_any = _buf_push_any_int
_buf_set = _buf_set_int
_buf_pop = _buf_pop_int

def _feb_adic_enc(src, buf, blen):
    c1 = 1
    c2 = 1
    while True:
        c1, c2 = _feb3_next(c1, c2)
        buf, blen = _buf_push_any(buf, blen, 1)
        if c2 > src:
            break
    #buf, blen = _buf_push(buf, blen, 1, 1)
    #cur = src - c2
    cur = src
    i = 0
    while c2 > 1:
        if cur >= c1:
            buf = _buf_set(buf, 1, i)
            cur -= c1
        else:
            buf = _buf_set(buf, 0, i)
        c1, c2 = _feb3_prev(c1, c2)
        i += 1
    assert cur == 0
    return buf, blen

def _feb_adic_dec(buf, blen, bla):
    c1 = 1
    c2 = 1
    val = 0
    while True:
        b = bla
        if b:
            val += c2
        c1, c2 = _feb3_next(c1, c2)
        if blen == 0:
            bla = 0
            blen = -1
            break
        buf, blen, bla = _buf_pop(buf, blen)
        if b and bla:
            break
    return val, buf, blen, bla

def _feb_unit_enc(cmd, val, buf, blen):
    buf, blen = _buf_push(buf, blen, (1 << (cmd + 1)) - 2, cmd + 1)
    buf, blen = _feb_adic_enc(val, buf, blen)
    return buf, blen

def _feb_unit_dec(buf, blen, bla):
    cmd = 0
    while True:
        b = bla
        cmd += b
        if blen == 0:
            bla = 0
            blen = -1
            break
        buf, blen, bla = _buf_pop(buf, blen)
        if not b:
            break
    if blen < 0:
        return cmd, None, buf, blen, bla
    val, buf, blen, bla = _feb_adic_dec(buf, blen, bla)
    return cmd, val, buf, blen, bla

def _feb_enc(seq, buf, blen):
    for val in seq:
        if isinstance(val, list):
            #TODO
            pass
        else:
            buf, blen = _feb_unit_enc(1, val, buf, blen)
    return buf, blen

def _feb_dec(buf, blen, bla):
    seq = []
    while blen >= 0:
        cmd, val, buf, blen, bla = _feb_unit_dec(buf, blen, bla)
        if cmd == 1:
            seq.append(val)
        else:
            #TODO
            pass
    return seq

if __name__ == '__main__':
    import pdb
    from hexdump import hexdump as hd
    from pprint import pprint
    ppr = lambda *a, **ka: pprint(*a, **ka, sort_dicts = False)

    def test1(n):
        for i in range(1, n+1):
            #cd, ln = _feb_adic_enc(i, 0, 0)
            cd, ln = _feb_unit_enc(1, i, 0, 0)
            cmd, dv, _, blen, _ = _feb_unit_dec(*_buf_pop(cd, ln))
            print(i, bin(cd), ln, '->', cmd, dv)
            assert cmd == 1 and dv == i and blen == -1
    #test1(20)

    def test2(n):
        seq = [i for i in range(1, n+1)]
        buf, blen = _feb_enc(seq, 0, 0)
        dseq = _feb_dec(*_buf_pop(buf, blen))
        print(buf, blen, seq, dseq)
        assert seq == dseq
        return buf
    buf = test2(20)
