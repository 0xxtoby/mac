#coding:utf-8
import codecs,binascii
import gmpy2,libnum
from Crypto.Util.number import long_to_bytes

n=87924348264132406875276140514499937145050893665602592992418171647042491658461
p=275127860351348928173285174381581152299
q=319576316814478949870590164193048041239
e=2
c=int('39DE036DE3132757E819F769EAD64BB487EE3F47E67843AFB73748FD9E979BE0',16)
# print(pow(2,2.4,4))



mp=pow(c,(p+1)/4,p)
mq=pow(c,(q+1)/4,q)
yp=gmpy2.invert(p,q)
yq=gmpy2.invert(q,p)
r=(yp*p*mq+yq*q*mp)%n
rr=n-r
s=(yp*p*mq-yq*q*mp)%n
ss=n-s
print(long_to_bytes(ss))
print(long_to_bytes(ss).decode())
print(long_to_bytes(rr))
print(long_to_bytes(rr).decode())

