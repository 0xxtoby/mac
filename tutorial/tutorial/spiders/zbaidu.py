import re

import scrapy
from scrapy import cmdline
from tutorial.items import TutorialItem

class ZbaiduSpider(scrapy.Spider):
    name = 'zbaidu'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ajavaee']

    def parse(self, response):
        item=TutorialItem()

        # print(response.body)
        li_lit=response.xpath('/html/body/div[10]/div/div[2]/ul/li')


        for li in li_lit:

            name_data=li.xpath('./div[2]/h2/text()')[0].extract()
            item['name']=name_data
            mask_data=li.xpath('./div[3]/p/text()')[0].extract()
            print(mask_data)
            # print(mask_data)
            item['mask']=mask_data

            yield item
            break


            # print(temp)


        # f=open('itcast.html','wb')
        # f.write(response.body)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl zbaidu --nolog".split())

#scrapy crawl zbaidu> --nolog