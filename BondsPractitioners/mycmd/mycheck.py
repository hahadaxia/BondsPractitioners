import os
import re
from scrapy.commands import ScrapyCommand
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import BondsPractitioners.settings as settings
from BondsPractitioners.models import SacModels as model
from BondsPractitioners.mycmd.myemail import send_email


class Command(ScrapyCommand):

    def short_desc(self):
        return "Check spiders"

    def run(self, args, opts):
        # 执行爬虫任务
        self.crawler_process.crawl('sac', **opts.__dict__)
        self.crawler_process.start()

        # 整理数据库，只保留最新一批数据，如最近一次任务失败，保留上一次任务结果
        session = sessionmaker(bind=create_engine(settings.CON_STR))()
        uptime_max = session.query(func.max(model.uptime)).first()
        session.query(model).filter(model.uptime != uptime_max[0]).delete()
        session.commit()

        # 查询最新的公司列表
        coms = [x.com.strip() for x in session.query(model.com).all()]
        session.close()

        self.check_spider(coms)
        send_email()

    def check_spider(self, coms):
        # 检查spiders下的spider是否具有基本的com_name和author,检查spiders的spider任务是否覆盖所有公司

        spider_py = [os.path.join(settings.SPIDERS_PATH, x)
                     for x in os.listdir(settings.SPIDERS_PATH) if not re.search(r'(__)|(sac)', x)]
        spider_coms = {x: y[1].strip() for x in spider_py
                       for y in re.findall(r"(com_name.*=.*)[\'\"](.*)[\'\"]", open(x, encoding='utf8').read())}
        spider_authors = {x: y[1] for x in spider_py
                          for y in re.findall(r"(author.*=.*)[\'\"](.*)[\'\"]", open(x, encoding='utf8').read())}

        # 检查com_name和author是否都有
        no_com = set(spider_py) - spider_coms.keys()
        no_author = set(spider_py) - spider_authors.keys()
        if no_com:
            print('no_com:', len(no_com), no_com)
        if no_author:
            print('no_author:', len(no_author), no_author)

        # 比较公司列表和爬虫列表，如有差异触发后续操作
        new_com = set(coms) - set(spider_coms.values())
        old_com = set(spider_coms.values()) - set(coms)
        if new_com:
            print('new_com:', len(new_com), new_com)
        if old_com:
            print('old_com:', len(old_com), old_com)
