# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BondsPractitioners.models import BondsPractitionersModels, SacModels
from datetime import datetime
from BondsPractitioners.mycmd.myemail import SCRAPY_RESULT


class PractitionerPipeline(object):
    def __init__(self, con_str, stats):
        self.con_str = con_str
        self.stats = stats

    @classmethod
    def from_crawler(cls, crawler):
        return cls(con_str=crawler.settings.get('CON_STR'), stats=crawler.stats, )

    def open_spider(self, spider):
        # 建立数据库连接
        self.uptime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.session = sessionmaker(bind=create_engine(self.con_str))()

    def process_item(self, item, spider):
        # 将item数据保存到数据库
        if spider.com_name == 'sac':
            model = SacModels()
        else:
            model = BondsPractitionersModels()

        for k, v in item.items():
            setattr(model, k, v)
            model.uptime = self.uptime
        self.session.add(model)

        return item

    def close_spider(self, spider):
        # 提交数据库修改，关闭数据库连接
        self.session.commit()
        self.session.close()

        # 提交爬取结果，用于后续统计处理
        SCRAPY_RESULT.append({'com': spider.com_name, 'author': spider.author,
                              'num': self.stats.get_stats().get('item_scraped_count')})
