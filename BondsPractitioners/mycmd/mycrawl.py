import csv
from ftplib import FTP
from scrapy.commands import ScrapyCommand
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

import BondsPractitioners.settings as settings
from BondsPractitioners.models import BondsPractitionersModels as model
from BondsPractitioners.mycmd.myemail import send_email


class Command(ScrapyCommand):

    def short_desc(self):
        return "Run spiders"

    def run(self, args, opts):
        # 获取爬虫列表，排除sac
        spiders_list = [x for x in self.crawler_process.spiders.list() if x != 'sac']

        # 遍历爬虫并执行任务
        for name in spiders_list:
            self.crawler_process.crawl(name, **opts.__dict__)
        self.crawler_process.start()

        # 整理数据库，每个公司只保留最新一批数据，如最近一次任务失败，保留上一次任务结果
        session = sessionmaker(bind=create_engine(settings.CON_STR))()
        dpl_com = session.query(model.com, func.max(model.uptime)).group_by(model.com).all()
        for com in dpl_com:
            session.query(model).filter(model.com == com[0], model.uptime != com[1]).delete()
        session.commit()

        data = [{k: v for k, v in m.__dict__.items() if not k.startswith('_')}
                for m in session.query(model).all()]
        session.close()

        self.up2ftp(data)

        send_email()

    def up2ftp(self, data):
        file_name = '债券投资交易人员信息.csv'
        # 生成csv文件
        with open(file_name, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            for d in data:
                writer.writerow(d)

        # 上传csv文件到ftp
        with FTP(settings.FTP_PARAM.get('host')) as ftp:
            ftp.login(settings.FTP_PARAM.get('user'), settings.FTP_PARAM.get('pwd'))
            with open(file_name, 'rb') as f:
                ftp_name = 'STOR ' + (settings.FTP_PARAM.get('dst_dir') + file_name).encode('GB2312').decode('latin-1')
                ftp.storbinary(ftp_name, f, 1024)
