# -*- coding: utf-8 -*-
import scrapy
from BondsPractitioners.spiders import set_item


class EwwwSpider(scrapy.Spider):
    name = 'ewww'
    allowed_domains = ['ewww.com.cn']
    start_urls = ['http://www.ewww.com.cn/departments/default.aspx?Skins=zxtzrygs']
    com_name = '渤海证券股份有限公司'
    author = 'huangkai'

    def parse(self, response):
        tables = response.xpath('//center/table')
        job = 'job'

        # 处理在职业务人员
        for tr in tables[0].xpath('./tr')[1:]:
            td = tr.xpath('./td/text()').getall()
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty'],
                               [self.com_name, '前台', '在职', job] + td[-3:])

        # 处理在职中后台人员
        for tr in tables[1].xpath('.//tr')[1:]:
            td = tr.xpath('./td/text()').getall()
            if len(td) == 5:
                job = td[0]
            if 4 <= len(td) <= 5:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty', 'phone'],
                               [self.com_name, '中后台', '在职', job] + td[-4:])

        # 处理离职人员
        for tr in tables[2].xpath('.//tr')[1:]:
            td = tr.xpath('./td/text()').getall()
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'state', 'name', 'ldate', 'dpt', 'duty'],
                               [self.com_name, '离职', job] + td[-3:])
