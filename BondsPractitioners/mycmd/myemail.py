from scrapy.mail import MailSender
import BondsPractitioners.settings as settings
from datetime import datetime

# 定义变量，用于接收所有爬虫处理结果
SCRAPY_RESULT = []


def send_email():
    # # 定义邮件发送器
    # mailer = MailSender(smtphost=settings.SMTP_HOST, mailfrom=settings.SMTP_USER,
    #                     smtpuser=settings.SMTP_USER, smtppass=settings.SMTP_PASS)
    #
    # # 处理爬虫结果，如有失败场景触发邮件通知
    # fails = ['公司：%s；维护人：%s；' % (x.get('com_name'), x.get('author')) for x in SCRAPY_RESULT if x.get('num') == 0]
    # if fails:
    #     subject = '爬虫失败「' + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + '」'
    #     mailer.send(to=settings.EMAIL_LIST, subject=subject, body='\n'.join(fails))
    print(SCRAPY_RESULT)
