import pprint

import requests
import re
import parser

# r=requests.get("http://www.baidu.com")
# print(r.text)


# User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

r = requests.get('https://bcy.net/item/detail/6892354076277742600', headers=headers)
# rs=requests.get('//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg',headers=headers)


# print(r.request.haders)
# print(rs.text)

print(r.text)


# html = r.text
#
# # <a href="//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg" alt="你与星河,皆可收藏" title="你与星河,皆可收藏">
# # <img alt="你与星河,皆可收藏-唯美女生" src="//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg" alt=""/></a>
#
# urls = re.findall('<a href="//(.*?)" alt=".*?" title=".*?">', html)
# # urls = re.findall('<dd><a href="(.*?)" >', html)
# print(urls)
# #


    # with open('img//' + file_name, mode='wb') as f:
    #     # print(url_data.content)
    #     f.write(url_data.content)
    #     print(file_name)
