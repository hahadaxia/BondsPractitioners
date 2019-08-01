# -*- coding: utf-8 -*-
import scrapy
import json


class SacSpider(scrapy.Spider):
    name = 'sac'
    allowed_domains = ['sac.net.cn']
    start_urls = ['http://sac.net.cn/']
    com_name = 'sac'
    author = 'huangkai'

    def start_requests(self):
        url = 'http://jg.sac.net.cn/pages/publicity/resource!search.action'
        headers = {'Content-Type': 'application/x-www-form-urlencoded',
                   'X-Requested-With': 'XMLHttpRequest'}
        body = ['filter_EQS_OTC_ID=1100&filter_LIKES_AOI_NAME=&sqlkey=publicity&sqlval=BONDTRADER_INFO',
                'filter_EQS_OTC_ID=1199&filter_LIKES_AOI_NAME=&sqlkey=publicity&sqlval=BONDTRADER_INFO',
                'filter_EQS_OTC_ID=20&filter_LIKES_AOI_NAME=&sqlkey=publicity&sqlval=BONDTRADER_INFO',
                'filter_EQS_OTC_ID=45&filter_LIKES_AOI_NAME=&sqlkey=publicity&sqlval=BONDTRADER_INFO']

        for b in body:
            yield scrapy.Request(url=url, method='POST', headers=headers, body=b, callback=self.parse)

    def parse(self, response):
        for r in json.loads(response.text):
            yield {'com': r.get('AOI_NAME'),
                   'url': r.get('BTI_PUBLICITY_PAGE_LINK')}
