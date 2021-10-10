import base64
import binascii

import libnum
from Crypto.Util.number import long_to_bytes
from scapy.compat import orb

import wiener_hack
def open_file_16(file_name,file_type):
     f=open(file_name,file_type)
     ff=f.read()
     hexstr = binascii.b2a_hex(ff)

     return hexstr



n=87924348264132406875276140514499937145050893665602592992418171647042491658461
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239
e = 65537
phi = (p-1)*(q-1)
d = libnum.invmod(e,phi)
c = int('6D3EB7DF23EEE1D38710BEBA78A0878E0E9C65BD3D08496DDA64924199110C79',16)
m = pow(c,d,n)
print(long_to_bytes(m))






nn = int("C2636AE5C3D8E43FFB97AB09028F1AAC6C0BF6CD3D70EBCA281BFFE97FBE30DD",16)


print(nn)