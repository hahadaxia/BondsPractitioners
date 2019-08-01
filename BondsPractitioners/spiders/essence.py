# -*- coding: utf-8 -*-
import scrapy
from BondsPractitioners.spiders import set_item


class EssenceSpider(scrapy.Spider):
    name = 'essence'
    allowed_domains = ['essence.com.cn']
    start_urls = ['http://www.essence.com.cn/emp/bond/']
    com_name = '安信证券股份有限公司'
    author = 'huangkai'

    def parse(self, response):
        # 处理在职人员
        for res in response.xpath("//div[@class='sr-wrap' or @class='asset-wrap']"):
            for r in res.xpath('.//tr')[1:]:
                td = r.xpath('.//td/text()').getall()
                yield set_item(['com', 'state', 'dpt', 'job', 'name', 'code', 'duty'],
                               [self.com_name, '在职'] + td)

        # 处理离职人员
        for res in response.xpath("//div[@class='departure-wrap']"):
            for r in res.xpath('.//tr')[1:]:
                td = r.xpath('.//td/text()').getall()
                yield set_item(['com', 'state', 'dpt', 'ldate', 'name', 'code', 'duty'],
                               [self.com_name, '离职'] + td)
