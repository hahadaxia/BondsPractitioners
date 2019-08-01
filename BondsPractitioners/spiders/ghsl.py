# -*- coding: utf-8 -*-
import scrapy
import pdfplumber
import os
from BondsPractitioners.spiders import set_item


class GhslSpider(scrapy.Spider):
    name = 'ghsl'
    allowed_domains = ['ghsl.cn']
    start_urls = ['http://www.ghsl.cn/PDF/Bond_traders.pdf']
    com_name = '北京高华证券有限责任公司'
    author = 'huangkai'

    def parse(self, response):
        # 获取返回数据，并保存为pdf文件
        file_path = self.settings.get('FILES_STORE')
        file_name = os.path.join(file_path, 'ghsl.pdf')
        with open(file_name, 'wb') as f:
            f.write(response.body)

        # 将保存的pdf文件整理为需处理的表格
        tables = []
        with pdfplumber.open(file_name) as pdf:
            for page in pdf.pages:
                for table in page.extract_tables():
                    tables.append([[r for r in row if r] for row in table])

        # 处理在职业务人员
        job = 'job'
        for td in tables[0][1:]:
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty'],
                               [self.com_name, '前台', '在职', job] + td[-3:])

        # 处理在职中后台人员
        for td in tables[1][1:]:
            if len(td) == 5:
                job = td[0]
            if 4 <= len(td) <= 5:
                yield set_item(['com', 'kind', 'state', 'job', 'name', 'dpt', 'duty', 'phone'],
                               [self.com_name, '中后台', '在职', job] + td[-4:])

        # 处理离职人员
        for td in tables[2][1:]:
            if len(td) == 4:
                job = td[0]
            if 3 <= len(td) <= 4:
                yield set_item(['com', 'state', 'name', 'ldate', 'dpt', 'duty'],
                               [self.com_name, '离职', job] + td[-3:])
