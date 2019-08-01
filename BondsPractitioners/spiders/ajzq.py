# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy import Selector
from BondsPractitioners.spiders import set_item


class AjzqSpider(scrapy.Spider):
    name = 'ajzq'
    allowed_domains = ['ajzq.com']
    start_urls = ['http://www.ajzq.com/service/mainArticle/15453']
    com_name = '爱建证券有限责任公司'
    author = 'huangkai'

    def parse(self, response):
        res = json.loads(response.text)['data']['content']
        tables = Selector(text=res).xpath('//table')
        job = 'job'

        # 处理在职业务人员
        for tr in tables[0].xpath('.//tr')[1:]:
            td = tr.xpath('.//td/p/span/text()').getall()
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty'],
                               [self.com_name, '前台', '在职', job] + td[-3:])

        # 处理在职中后台人员
        for tr in tables[1].xpath('.//tr')[1:]:
            td = tr.xpath('.//td/p/span/text()').getall()
            if len(td) == 5:
                job = td[0]
            if 4 <= len(td) <= 5:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty', 'phone'],
                               [self.com_name, '中后台', '在职', job] + td[-4:])

        # 处理离职人员
        for tr in tables[2].xpath('.//tr')[1:]:
            td = tr.xpath('.//td/p/span/text()').getall()
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'state', 'name', 'ldate', 'dpt', 'duty'],
                               [self.com_name, '离职', job] + td[-3:])
