from Crypto.Util.number import bytes_to_long, long_to_bytes

import wiener_hack
import gmpy2

e=65537
n=int("A9BD4C7A7763370A042FE6BEC7DDC841602DB942C7A362D1B5D372A4D08912D9",16)

p=273821108020968288372911424519201044333
q=280385007186315115828483000867559983517

f_c=open("/Users/oo/Downloads/RSA256/fllllllag.txt","rb").read()
c=bytes_to_long(f_c)
d=gmpy2.invert(e,(p - 1) * (q - 1))


m=pow(c,d,n)
print(long_to_bytes(m))


