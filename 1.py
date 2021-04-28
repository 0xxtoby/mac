# encrypt
from Crypto.Util.number import bytes_to_long, long_to_bytes, inverse
from Crypto.Util.number import getPrime
from gmpy2 import invert
flag = b"test.......test"
e = 65537
# getPrime(512) 512bit
p = getPrime(512)
q = getPrime(512)
n = p*q
# bytes_to_long bytes->num
m = bytes_to_long(flag)
c = pow(m, e, n)
print(c)