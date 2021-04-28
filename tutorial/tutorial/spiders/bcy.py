import scrapy


class BcySpider(scrapy.Spider):
    name = 'bcy'
    # allowed_domains = ['bcy.cn']
    start_urls = ['https://bcy.net/item/detail/6894058022042082308?_source_page=cos']

    def parse(self, response):
        print(response.body)
        f=open('pcy.html','wb')
        f.write(response.body)
