#!/usr/bin/python
#coding:utf-8
import gmpy2
from Crypto.Util.number import long_to_bytes

#已知
n = 920139713
e = 19



p = 49891
q = 18443

phi = (p-1)*(q-1)
d = gmpy2.invert(e,phi)
m = b""
with open('roll.txt','r') as f:
    for c in f.readlines():
        print(pow(int(c), d, n))
        m = m +  long_to_bytes(pow(int(c), d, n))
print(m)