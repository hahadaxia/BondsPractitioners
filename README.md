# BondsPractitioners
获取证券公司债券投资交易人员信息

### 新增spider说明

1. 使用 scrapy genspider 生成一个新的爬虫任务，为避免名称重复，爬虫名称建议使用url中的一级域名，例如爱建证券有限责任公司，一级域名为www.ajzq.com，爬虫名称建议命名为ajzq
2.  回到生成的爬虫任务代码，添加两个必要变量，com_name（公司名称）和author（作者），其中公司名称应使用sac.csv中的标准名称，作者填写自己的姓名
3. 在spider代码中写业务逻辑，需爬取内容参考items.py文件下的PractitionerItem，item赋值过程可以使用spiders包内的标准方法set_item

### 功能使用介绍

1. 调试单个爬虫，可以使用标准命令scrapy crawl XXXX，执行后会在BondsPractitioners.db中新增此次爬取结果
2. 如需批量运行爬虫，可以使用自定义命令 scrapy mycrawl
   - 此命令会批量执行spiders下的所有爬虫
   - 在BondsPractitioners.db中插入执行结果
   - 比对数据库，按公司保留最新一批次执行结果
   - 导出最新结果为csv文件
   - 触发通知任务（如有）
3. 如需检查爬虫是否合规，可以使用自定义命令scrapy mycheck
   - 此命令会触发一次sac爬虫任务并将最新数据保存在数据库
   - 检查spiders目录下的爬虫com_name和author是否合规
   - 对比spiders和sac中的公司名称，找到差异
   - 触发通知任务（如有）