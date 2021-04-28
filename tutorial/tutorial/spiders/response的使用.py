import pprint
import re

import scrapy
from scrapy import cmdline


class ZbaiduSpider(scrapy.Spider):
    name = 'restext'
    # allowed_domains = ['baidu.com']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml#ajavaee']

    def parse(self, response):
        # print(response.body)
        li_lit=response.xpath('/html/body/div[10]/div/div[2]/ul/li')


        for li in li_lit:
            temp={}
            name_data=li.xpath('./div[2]/h2/text()')[0].extract()
            temp['name']=name_data
            mask_data=li.xpath('./div[3]/p/text()')[0].extract()
            # print(mask_data)
            temp['mask']=mask_data

            yield temp


            # print(temp)


        #=======response 的基本方法======
        print(response.url)                 #当前响应url
        print(response.request.url)         #当前响应对应的url
        pprint.pprint(response.headers)             #响应头
        pprint.pprint(response.request.headers)     #当前响应对应的响应头
        # print(response.body)                #响应体  html代码
        print(response.status)              #状态响应码


        # f=open('itcast.html','wb')
        # f.write(response.body)


if __name__ == '__main__':
    cmdline.execute("scrapy crawl restext --nolog".split())

#scrapy crawl zbaidu> --nolog