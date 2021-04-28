import os
import pprint

import requests
import re
import parser

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'
}

home_url = requests.get('https://www.vmgirls.com/archives.html', headers=headers)
html = home_url.text
print(html)
# <a href=15444.html title="好漂亮的花呀" target=_blank class="list-title text-sm h-2x">好漂亮的花呀</a>
# <a target="_blank" style="color: #e83e8c;" href="15931.html">欢迎来到我的世界</a>
jpg_list = re.findall('<a target=_blank style="color: #e83e8c;" href=(.*?)>', html)
print(jpg_list)

#
def mkdir(path):
    # 引入模块
    import os
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)
        print
        path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        print
        path + ' 目录已存在'
        return False



for jpg in jpg_list:

    r = requests.get(f'https://www.vmgirls.com/{jpg}', headers=headers)

    html = r.text

    urls = re.findall('<a href="//(.*?)" alt=".*?" title=".*?">', html)
    print(urls)

    # os.makedirs(f'img//{jpg}')
    if(mkdir(f'img//{jpg}')):

        for url in urls:
            headers_jpg = {
                'Referer': f'https://www.vmgirls.com/{jpg}'
                , 'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.16; rv:84.0) Gecko/20100101 Firefox/84.0'

            }
            url_data = requests.get('https://' + url, headers=headers_jpg)

            # 数据保存
            file_name = url.split('/')[-1]


            with open(f'img//{jpg}//' + file_name, mode='wb') as f:
                f.write(url_data.content)
                print('创建成功'+file_name)
