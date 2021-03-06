# CalHamletV1.py
def getText():
    txt = open("hamlet.TXT", "r", encoding='UTF-8').read()  # 打开文件
    txt = txt.lower()  # 全部转成小写
    for ch in '!"#$%&()*+,-./:;<=>?@[\\]^_‘{|}~':
        txt = txt.replace(ch, " ")  # 将文本中特殊字符替换为空格
    return txt


hamletTxt = getText()
words = hamletTxt.split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
items = list(counts.items())
items.sort(key=lambda x: x[1], reverse=True)  # 排序
for i in range(10):
    word, count = items[i]
    print("{0:<10}{1:>5}".format(word, count))
