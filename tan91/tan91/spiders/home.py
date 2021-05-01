import re

import scrapy
from scrapy import cmdline

from tan91.items import Tan91Item
from tan91.settings import IMAGES_STORE


class HomeSpider(scrapy.Spider):
    name = 'home'

    def start_requests(self):
        url = [
            'https://www.sehuatang.net/search.php?mod=forum&searchid=70094&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%E6%B0%B8%E7%80%AC%E3%82%86%E3%81%84']

        yield scrapy.Request(url=url[0], callback=self.parse, meta={'i': 1, })
        # yield scrapy.Request(url=url[1], callback=self.parse,meta={'i':1,})

        # for i in range(2, 4):
        #     url_s = f'https://www.sehuatang.net/search.php?mod=forum&searchid=349210&orderby=lastpost&ascdesc=desc&searchsubmit=yes&page={i}'
        #     yield scrapy.Request(url=url_s, callback=self.parse, meta={'i': i, })
        #     break

    def parse(self, response):
        f = open(f'{IMAGES_STORE}/html//home//{response.meta["i"]}.html', 'wb')
        print(response.body)
        f.write(response.body)

        next_url = response.xpath('/html/body/div[5]/div/div/div[2]/ul/li/h3/a/@href').extract()
        print(next_url)

        item = Tan91Item()
        for url in next_url:
            u = 'https://www.sehuatang.net/' + url
            id = re.findall('&tid=(.*?)&', url)[0]
            print(id)
            item['id'] = id
            item['next_url'] = u

            yield scrapy.Request(url=u, callback=self.next_url, meta={'item': item})
            break

    def next_url(self, response):
        f=open(f'{IMAGES_STORE}//html//next//{response.meta["item"]["id"]}.html','wb')
        f.write(response.body)
        # print(response.body)

        item = response.meta['item']
        try:
            name_data=response.xpath('//*[@id="thread_subject"]/text()')[0].extract()
            item['name'] = name_data
            print(name_data)
        except Exception as response:
            print('name读取错误')


        try:
            data=response.xpath('//*[@class="t_f"]/text()').extract()
            zdata=''
            for d in data:
                if d!='':
                    zdata=zdata+d
            print(zdata)
        except Exception as response:
            print('data 错误')



        try:
            jpg_url=response.xpath('//*[@class="t_f"]//img/@file').extract()

            print(jpg_url)
        except Exception as response:
            print('jpg_url 错误')













if __name__ == '__main__':
    cmdline.execute("scrapy crawl home  ".split())

