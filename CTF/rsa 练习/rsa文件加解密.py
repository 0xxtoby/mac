from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_cipher
import base64

random_generator = Random.new().read
rsa = RSA.generate(2048, random_generator)

private_key = rsa.exportKey()
with open("private_a.rsa", 'wb') as f:
    f.write(private_key)

public_key = rsa.publickey().exportKey()
with open("public_a.rsa", 'wb') as f:
    f.write(public_key)

# 使用公钥对内容进行rsa加密
message = "需要加密的信息"
with open('public_a.rsa') as f:
    key = f.read()
    pub_key = RSA.importKey(str(key))
    cipher = PKCS1_cipher.new(pub_key)
    rsa_text = base64.b64encode(cipher.encrypt(bytes(message.encode("utf8"))))
    print(rsa_text.decode('utf-8'))

# 使用私钥对内容进行rsa解密
with open('private_a.rsa') as f:
    key = f.read()
    pri_key = RSA.importKey(key)
    cipher = PKCS1_cipher.new(pri_key)
    back_text = cipher.decrypt(base64.b64decode(rsa_text), 0)
    print(back_text.decode('utf-8'))