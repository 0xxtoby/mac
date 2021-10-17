# coding=utf-8
#生成RSA公钥和私钥
import pprint

from Crypto import Random
from Crypto.PublicKey import RSA

random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)
# 生成私钥
private_key = rsa.exportKey()
print(private_key.decode('utf-8'))
print("-" * 30 + "分割线" + "-" * 30)
# 生成公钥
public_key = rsa.publickey().exportKey()
print(public_key.decode('utf-8'))

import  keyword
pprint.pprint(keyword.kwlist)