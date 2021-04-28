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

r = requests.get('https://www.vmgirls.com/12945.html', headers=headers)
# rs=requests.get('//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg',headers=headers)


# print(r.request.haders)
# print(rs.text)

# print(r.text)


html = r.text

# <a href="//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg" alt="你与星河,皆可收藏" title="你与星河,皆可收藏">
# <img alt="你与星河,皆可收藏-唯美女生" src="//t.cdn.ink/image/2020/01/2020020916481695-scaled.jpeg" alt=""/></a>

urls = re.findall('<a href="//(.*?)" alt=".*?" title=".*?">', html)
# urls = re.findall('<dd><a href="(.*?)" >', html)
print(urls)
#
for url in urls:

    headers_jpg = {
        'Referer': 'https://www.vmgirls.com/12945.html'
        ,'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'

    }
    url_data = requests.get('https://' + url, headers=headers_jpg)




#     # <a class="btn btn-default btn-xs" href="https://i.hexuexiao.cn/up/34/dd/26/6bf1e593e757e5f6169768c75f26dd34.jpg.source.jpg" role="button" target="_blank">
#     jpgs = re.findall('<a class="btn btn-default btn-xs" href="(.*?)" role="button" target="_blank">', html_data)
#     print(jpgs)
#     img_data = requests.get(jpgs[0], headers=headers).content
#     # print(img_data)
    # 数据保存
    file_name = url.split('/')[-1]

    with open('唯美女生/img//' + file_name, mode='wb') as f:
        f.write(url_data.content)
        print(file_name)
