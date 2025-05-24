# Enhanced Fibonacci Coding

Fibonacci coding for nested non-negative integer sequence.

## Example

```python
from efc import efc_enc, efc_dec

seq = [[[[1, 2], 3], 4], [5, [6, [7, [8, [9, 10]]], 11]], [[12, 13], 14, 15, [16, 17]]]
buf, blen = efc_enc(seq)
print(hex(buf), blen) # 0x3198f6bd87bb4ecbb0768ec98bc6af3981a1ec8c4ed4c2f1 190

dseq = efc_dec(buf, blen)
assert seq == dseq
```
