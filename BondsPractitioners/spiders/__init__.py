# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
from BondsPractitioners.items import PractitionerItem
import logging
import platform
import os
from os.path import dirname, abspath

logger = logging.getLogger(__name__)


def set_item(klist, vlist):
    if len(klist) != len(vlist):
        logger.error('输入列表长度不同，无法完成赋值')
        return None
    try:
        item = PractitionerItem()
        for num, key in enumerate(klist):
            item[key] = vlist[num]
        return item
    except Exception as e:
        logging.error(e)


def doc2docx(filename):
    if not filename.endswith('doc'):
        return
    os_name = platform.system()
    doc_file = os.path.join(dirname(dirname(dirname(abspath(__file__)))), filename)

    # Linux系统安装OpenOffice或者LibreOffice，安装unoconv
    if os_name == 'Linux':
        import subprocess
        subprocess.call('unoconv -f docx ' + doc_file, shell=True)

    # Windows系统需要安装MicrosoftOffice
    if os_name == 'Windows':
        from win32com import client
        word = client.Dispatch('Word.Application')
        doc = word.Documents.Open(doc_file)
        doc.SaveAs(doc_file + 'x', 16)
        doc.Close()
        word.Quit()
