# -*- coding: utf-8 -*-
import json
import re
import time

import scrapy

from ..items import TaobaoProItem
from taobao_pro.models.MySQLModel import  tb_mysql
from ..def_packages import get_cookie,handle_click_url,tb_log,handle_next_url
from ..selenium_taobao import  tb_selenium


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com','s.taobao.com']
    # start_urls = ['http://taobao.com/']
    header = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "sec - fetch - mode": "navigate",
        "sec - fetch - site": "same - origin",
        "sec - fetch - user": "?1",
        "upgrade - insecure - requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36",
    }
    data_count = 0
    text = ""
    value = ""

    def start_requests(self):
        try:
            task_list = tb_mysql.get_index_category()
            for task in task_list:
                info_dict = {}
                info_dict['main_category'] = task[1]
                info_dict['second_category_name'] = task[2]
                info_dict['category_name'] = task[3]
                info_dict['category_href'] = task[0]
                yield scrapy.Request(
                    # 发送请求的URL
                    url = task[0],
                    # 要携带的cookie信息
                    cookies = get_cookie(task[0]),
                    # 请求头
                    headers=self.header,
                    # 回调函数
                    callback = self.first_parse,
                    # 字典的格式，向其他方法里面传递信息
                    meta = info_dict
                )
        except:
            tb_selenium.main()
            self.start_requests()

    def first_parse(self,response):
        p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
        result = p.search(response.text).group(1)
        json_data = json.loads(result)
        pageSize = json_data['mods']['sortbar']['data']['pager']['pageSize']
        totalPage = json_data['mods']['sortbar']['data']['pager']['totalPage']
        totalCount = json_data['mods']['sortbar']['data']['pager']['totalCount']
        tb_log("{category_name}:总数{totalcount}".format(totalcount=totalCount,category_name=response.request.meta['category_name']))
        if totalCount > totalPage * pageSize:
            for item in json_data['mods']['nav']['data']['common'][0]['sub']:
                info_dict = {}
                info_dict['main_category'] = response.request.meta['main_category']
                info_dict['second_category_name'] = response.request.meta['second_category_name']
                info_dict['category_name'] = response.request.meta['category_name']
                info_dict['category_href'] = response.request.meta['category_href']
                p_text = json_data['mods']['nav']['data']['common'][0]['text']
                v_text = item['text']
                info_dict['text'] = p_text + ":" + v_text
                info_dict['value'] = item['value']
                click_url = handle_click_url(response.request.meta['category_href'], info_dict['value'], 0)
                yield scrapy.Request(url=click_url,callback=self.parse_page,meta=info_dict,headers=self.header)
        else:
            try:
                vlaue_exist = response.request.meta['value']
            except:
                vlaue_exist = None
            if vlaue_exist == None:
                response.request.meta['category_text'] = response.request.meta['category_name']
            yield scrapy.Request(url=response.request.url, callback=self.parse_data, meta=response.request.meta,headers=self.header, dont_filter=True)

    def parse_page(self, response):
        p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
        result = p.search(response.text).group(1)
        json_data = json.loads(result)
        pageSize = json_data['mods']['sortbar']['data']['pager']['pageSize']
        totalPage = json_data['mods']['sortbar']['data']['pager']['totalPage']
        totalCount = json_data['mods']['sortbar']['data']['pager']['totalCount']
        if totalCount > totalPage * pageSize:
            try:
                commom_have = json_data['mods']['nav']['data']['common']
            except:
                commom_have = None
            if commom_have != None:
                for item in json_data['mods']['nav']['data']['common'][0]['sub']:
                    info_dict = {}
                    info_dict['main_category'] = response.request.meta['main_category']
                    info_dict['second_category_name'] = response.request.meta['second_category_name']
                    info_dict['category_name'] = response.request.meta['category_name']
                    info_dict['category_href'] = response.request.meta['category_href']
                    p_text = json_data['mods']['nav']['data']['common'][0]['text']
                    v_text = item['text']
                    info_dict['text'] = response.request.meta['text'] + ";" + p_text + ":" + v_text
                    info_dict['value'] = response.request.meta['value'] + ";" + item['value']
                    click_url = handle_click_url(response.request.meta['category_href'], info_dict['value'], 0)
                    yield scrapy.Request(url=click_url, callback=self.parse_page, meta=info_dict,headers=self.header)
            else:
                yield scrapy.Request(url=response.request.url, callback=self.parse_data, meta=response.request.meta, headers=self.header,dont_filter=True)
        else:
            yield scrapy.Request(url=response.request.url, callback=self.parse_data, meta=response.request.meta, headers=self.header,dont_filter=True)

    def parse_data(self, response):
        p = re.compile(r'g_page_config = (\{.+\});\s*', re.M)
        result = p.search(response.text).group(1)
        json_data = json.loads(result)
        pageSize = json_data['mods']['sortbar']['data']['pager']['pageSize']
        totalPage = json_data['mods']['sortbar']['data']['pager']['totalPage']
        currentPage = json_data['mods']['sortbar']['data']['pager']['currentPage']
        totalCount = json_data['mods']['sortbar']['data']['pager']['totalCount']
        nowPageTotal = json_data['mods']['p4p']['data']['p4pconfig']['auction_num']['search']
        try:
            text = response.request.meta['text']
        except:
            text = response.request.meta['category_text']
        tb_log(response.request.meta['category_name'] +": " + text + "。 当前第{0}页，页面数据长度{1}条，总页数{2}页，总数据量{3}条,当前页面数据量{4}。".format(currentPage, pageSize, totalPage, totalCount,nowPageTotal))
        if totalCount != 0:
            for item in json_data['mods']['itemlist']['data']['auctions']:
                info_dict = TaobaoProItem()
                info_dict['main_category'] = response.request.meta['main_category']
                info_dict['second_category_name'] = response.request.meta['second_category_name']
                info_dict['category_name'] = response.request.meta['category_name']
                info_dict['category_href'] = response.request.meta['category_href']
                info_dict['v_text'] = text
                info_dict['goods_id'] = int(item['nid'])
                info_dict['title'] = item['raw_title']
                info_dict['price'] = item['view_price']
                info_dict['local'] = item['item_loc']
                info_dict['view_sales'] = item['view_sales']
                try:
                    info_dict['comment_count'] = int(item['comment_count'])
                except:
                    info_dict['comment_count'] = 0
                info_dict['user_id'] = int(item['user_id'])
                info_dict['nick'] = item['nick']
                if "https" in item['detail_url']:
                    info_dict['good_url'] = item['detail_url']
                else:
                    info_dict['good_url'] = "https:" + item['detail_url']
                info_dict['crawl_time'] = time.strftime("%Y--%m--%d %H:%M:%S", time.localtime(time.time()))
                yield info_dict
                self.data_count += 1
            data_text = "成功入库数据{data_count}条.".format(data_count=self.data_count)
            tb_log(data_text)
            print(data_text)
        if currentPage < totalPage:
            try:
                if response.request.meta['text']:
                    next_url = handle_click_url(response.request.meta['category_href'],response.request.meta['value'], pageSize * currentPage)
            except:
                if response.request.meta['category_text']:
                    next_url = handle_next_url(response.request.meta['category_href'], pageSize * currentPage)
            yield scrapy.Request(url=next_url, callback=self.parse, meta=response.request.meta,headers=self.header)
