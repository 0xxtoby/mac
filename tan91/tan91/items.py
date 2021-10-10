# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Tan91Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    user_name = scrapy.Field()
    id = scrapy.Field()

    att_url = scrapy.Field()
    att_name = scrapy.Field()

    jpgs = scrapy.Field()
    blockcode = scrapy.Field()
    search = scrapy.Field()
    html_data = scrapy.Field()



    data = scrapy.Field()
    next_url = scrapy.Field()

    seiz = scrapy.Field()