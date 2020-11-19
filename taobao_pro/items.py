# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TaobaoProItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 商品ID
    goods_id = scrapy.Field()
    # 商品标题
    title = scrapy.Field()
    # 商品价格
    price = scrapy.Field()
    # 卖家所在地
    local = scrapy.Field()
    # 筛选信息
    v_text = scrapy.Field()
    # 收货人数
    view_sales = scrapy.Field()
    # 评论人数
    comment_count = scrapy.Field()
    # 卖家用户ID
    user_id = scrapy.Field()
    # 卖家昵称
    nick = scrapy.Field()
    # 商品详情页url
    good_url = scrapy.Field()
    # 主类别
    main_category = scrapy.Field()
    # 第二类别
    second_category_name = scrapy.Field()
    # 类别名称
    category_name = scrapy.Field()
    # 类别链接
    category_href = scrapy.Field()
    # 抓取日期
    crawl_time = scrapy.Field()
