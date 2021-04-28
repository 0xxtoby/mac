# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import json

from itemadapter import ItemAdapter


class TutorialPipeline(object):
    # def __init__(self):
    #     self.file=open('tutorial/date/pcy.json','w')  #   w写
    #                                                 #   wb写二进制文件
    #                                                 #   a 文件内容追加

    def process_item(self, item, spider):

        print('guandao:',item)
        # 字典序列化
        # 将item对象强转成字典
        item=dict(item)


        json_data=json.dumps(item,ensure_ascii=False)+',\n'
        # print(json_data)
        # self.file.write(json_data)


        #默认使用完管道需要把数据返回引擎
        return item

    # def __del__(self):
    #     self.file.close()
