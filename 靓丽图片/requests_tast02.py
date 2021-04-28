import requests
import re
import parser

for page in range(1,12):

    print(f'=============正在读取第{page}页==================')


    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'
    }

    r = requests.get(f'https://www.hexuexiao.cn/meinv/guzhuang/list-{page}.html', headers=headers)


    html = r.text


    urls = re.findall('<dd><a href="(.*?)" >', html)
    print(urls)

    for url in urls:
        html_data = requests.get(url, headers=headers).text
        # <a class="btn btn-default btn-xs" href="https://i.hexuexiao.cn/up/34/dd/26/6bf1e593e757e5f6169768c75f26dd34.jpg.source.jpg" role="button" target="_blank">
        jpgs = re.findall('<a class="btn btn-default btn-xs" href="(.*?)" role="button" target="_blank">', html_data)
        print(jpgs)
        img_data = requests.get(jpgs[0], headers=headers).content
        # print(img_data)
        # 数据保存
        file_name = jpgs[0].split('/')[-1]

        with open('img//' + file_name, mode='wb') as b:
            b.write(img_data)
            print(file_name)
