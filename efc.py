#! python3
# coding: utf-8

# Enhanced Fibonacci Coding

def _fib3_next(c1, c2):
    return c2, c1 + c2

def _fib3_prev(c1, c2):
    return c2 - c1, c1

def _buf_new_int():
    return 0, 0

def _buf_push_int(buf, blen, v, n):
    return (buf << n) | v, blen + n

def _buf_push_any_int(buf, blen, n):
    return buf << n, blen + n

def _buf_set_int(buf, v, n):
    return buf | (v << n)

def _buf_pop_int(buf, blen):
    return buf, blen - 1, (buf >> (blen - 1)) & 1

_buf_new = _buf_new_int
_buf_push = _buf_push_int
_buf_push_any = _buf_push_any_int
_buf_set = _buf_set_int
_buf_pop = _buf_pop_int

def _fib_adic_enc(src, buf, blen):
    assert src > 0
    c1 = 1
    c2 = 1
    while True:
        c1, c2 = _fib3_next(c1, c2)
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
        c1, c2 = _fib3_prev(c1, c2)
        i += 1
    assert cur == 0
    return buf, blen

def _fib_adic_dec(buf, blen, bla):
    c1 = 1
    c2 = 1
    val = 0
    while True:
        b = bla
        if b:
            val += c2
        c1, c2 = _fib3_next(c1, c2)
        if blen == 0:
            bla = 0
            blen = -1
            break
        buf, blen, bla = _buf_pop(buf, blen)
        if b and bla:
            break
    return val, buf, blen, bla

def _fib_unit_enc(cmd, val, buf, blen):
    buf, blen = _buf_push(buf, blen, (1 << (cmd + 1)) - 2, cmd + 1)
    buf, blen = _fib_adic_enc(val, buf, blen)
    return buf, blen

def _fib_unit_dec(buf, blen, bla):
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
    val, buf, blen, bla = _fib_adic_dec(buf, blen, bla)
    return cmd, val, buf, blen, bla

def _fib_seq_enc(seq, buf, blen, prv_ilvl):
    ilvl = prv_ilvl
    olvl = 0
    for val in seq:
        if olvl > 0:
            buf, blen = _fib_unit_enc(3, olvl, buf, blen)
            olvl = 0
        if isinstance(val, list):
            buf, blen, olvl = _fib_seq_enc(val, buf, blen, ilvl + 1)
        else:
            if ilvl > 0:
                buf, blen = _fib_unit_enc(2, ilvl, buf, blen)
            buf, blen = _fib_unit_enc(1, val+1, buf, blen)
        ilvl = 0
    return buf, blen, olvl + 1

def _fib_seq_dec(buf, blen, bla, prv_ilvl):
    seq = []
    ilvl = prv_ilvl
    olvl = 0
    while True:
        if ilvl > 0:
            sseq, olvl, buf, blen, bla = _fib_seq_dec(buf, blen, bla, ilvl - 1)
            seq.append(sseq)
            ilvl = 0
        if olvl > 0:
            return seq, olvl - 1, buf, blen, bla
        if blen < 0:
            break
        cmd, val, buf, blen, bla = _fib_unit_dec(buf, blen, bla)
        if cmd == 1:
            seq.append(val-1)
        elif cmd == 2:
            ilvl = val
        elif cmd == 3:
            olvl = val
        else:
            raise ValueError('unknown command:', cmd)
    return seq, olvl, buf, blen, bla

def _fib_enc(seq):
    buf, blen, olvl = _fib_seq_enc(seq, *_buf_new(), 0)
    if olvl > 0:
        buf, blen = _fib_unit_enc(3, olvl, buf, blen)
    return buf, blen

def _fib_dec(buf, blen):
    seq, olvl, buf, blen, bla = _fib_seq_dec(*_buf_pop(buf, blen), 0)
    assert olvl == 0 and blen == -1 and bla == 0
    return seq

efc_enc = _fib_enc
efc_dec = _fib_dec

if __name__ == '__main__':
    import pdb
    from hexdump import hexdump as hd
    from pprint import pprint
    ppr = lambda *a, **ka: pprint(*a, **ka, sort_dicts = False)

    def test1(n):
        for i in range(1, n+1):
            #cd, ln = _fib_adic_enc(i, 0, 0)
            cd, ln = _fib_unit_enc(1, i, 0, 0)
            cmd, dv, _, blen, _ = _fib_unit_dec(*_buf_pop(cd, ln))
            print(i, bin(cd), ln, '->', cmd, dv)
            assert cmd == 1 and dv == i and blen == -1
    #test1(20)

    def test2(n):
        seq = [i for i in range(1, n+1)]
        buf, blen = _fib_enc(seq, 0, 0)
        dseq = _fib_dec(*_buf_pop(buf, blen))
        print(buf, blen, seq, dseq)
        assert seq == dseq
        return buf
    #buf = test2(20)

    def test3():
        seq = [[[[1, 2], 3], 4], [5, [6, [7, [8, [9, 10]]], 11]], [[12, 13], 14, 15, [16, 17]]]
        buf, blen = _fib_enc(seq)
        dseq = _fib_dec(buf, blen)
        print(buf, blen, seq, dseq)
        assert seq == dseq
        return buf
    #buf = test3()
