# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BondspractitionersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class CompanyItem(scrapy.Item):
    pass


class PractitionerItem(scrapy.Item):
    # 公司
    com = scrapy.Field()
    # 部门
    dpt = scrapy.Field()
    # 岗位
    job = scrapy.Field()
    # 姓名
    name = scrapy.Field()
    # 职务
    duty = scrapy.Field()
    # 状态(在职、离职)
    state = scrapy.Field()
    # 分类（前台、中后台）
    kind = scrapy.Field()
    # 电话
    phone = scrapy.Field()
    # 离职日期
    ldate = scrapy.Field()
    # 资格编码
    code = scrapy.Field()
    # 其它
    other = scrapy.Field()
