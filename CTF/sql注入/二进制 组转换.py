import re

from libnum import s2b

s='''11 111 010 000 0 1010 111 100 0 00 000 000 111 00 10 1 0 010 0 000 1 00 10 110'''

b=re.findall("\w*",s)
ii=''
for i in b:
    if i != "":
        ii=ii+i
cc=int(ii,2)

print(ii)
print(b)