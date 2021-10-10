import re

import scrapy
from scrapy import cmdline

from tan91.items import Tan91Item
from tan91.settings import IMAGES_STORE


class HomeSpider(scrapy.Spider):
    name = 'home'

    def start_requests(self):
        url = [
            'https://www.sehuatang.net/search.php?mod=forum&searchid=102930&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=%E6%B0%B8%E7%80%AC%E3%82%86%E3%81%84'
            ,'https://www.sehuatang.net/forum-37-1.html'
        ]


        # yield scrapy.Request(url=url[1], callback=self.parse, meta={'i': 1, })
        # yield scrapy.Request(url=url[1], callback=self.parse,meta={'i':1,})

        for i in range(1,424):
            url_s = f'https://www.sehuatang.net/forum-103-{i}.html'
            yield scrapy.Request(url=url_s, callback=self.parse, meta={'i': i, })
            # break

    def parse(self, response):
        # f = open(f'{IMAGES_STORE}/html//home//{response.meta["i"]}.html', 'wb')
        # print(response.body)
        # f.write(response.body)

        # next_url = response.xpath('/html/body/div[5]/div/div/div[2]/ul/li/h3/a/@href').extract()
        next_url = response.xpath('/html/body/div[6]/div[6]/div/div/div[4]/div[2]/form/table/tbody[position()>8]/tr/th/a[2]/@href').extract()
        print(next_url)


        for url in next_url:
            u = 'https://www.sehuatang.net/' + url
            # id = re.findall('&tid=(.*?)&', url)[0]
            id = url.split('-')[1]
            print(id)

            yield scrapy.Request(url=u, callback=self.next_url, meta={'id':id,'next_url':u})
            # break

    def next_url(self, response):
        item = Tan91Item()

        # f=open(f'{IMAGES_STORE}//html//next//{response.meta["id"]}.html','wb')
        # f.write(response.body)
        # # print(response.body)

        item['id']=response.meta['id']
        item['next_url']=response.meta['next_url']
        item['search']='高清中文字幕'

        item['html_data']=response.text
        try:
            name_data=response.xpath('//*[@id="thread_subject"]/text()')[0].extract()
            item['name'] = name_data
            # print(name_data)
        except Exception as response:
            print('name读取错误')
            item['name'] = ''



        try:
            data=response.xpath('//*[@class="t_f"]/text()').extract()
            zdata=''

            for d in data:
                if d!='' and not d=='\n':
                    zdata=zdata+d

            # print(zdata)
            item['data']=zdata
        except Exception as response:
            print('data 错误')
            item['data'] = ''



        try:
            jpgs=response.xpath('//*[@class="t_f"]//img/@file').extract()

            # print(jpgs)
            item['jpgs']=jpgs
        except Exception as response:
            try:
                jpgs = response.xpath('//*[@class="t_f"]//img/@src').extract()

                # print(jpgs)
                item['jpgs'] = jpgs
            except Exception as response:
                print('无照片')
                item['jpgs'] = ''

        try:
            bt=response.xpath('//*[@class="blockcode"]//li/text()')[0].extract()

            # print(bt)
            item['blockcode']=bt
        except Exception as response:
            print('bt无')
            item['blockcode'] = ''

        try:
            attum_url=response.xpath('//*[@class="attnm"]//a/@href')[0].extract()
            attum_name=response.xpath('//*[@class="attnm"]//a/text()')[0].extract()

            # print(attum_name,attum_url)

            item['att_url']=attum_url
            item['att_name']=attum_name
        except Exception as response:
            print('附件 无')
            item['att_url'] = ''
            item['att_name'] = ''


        yield  item

















if __name__ == '__main__':
    cmdline.execute("scrapy crawl home --nolog".split())

