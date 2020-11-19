# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from taobao_pro.models.MySQLModel import tb_mysql

class TaobaoProPipeline:
    def process_item(self, item, spider):
        tb_mysql.goods_data(item)
        return item
