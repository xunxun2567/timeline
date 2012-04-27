# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://my.yingjiesheng.com/ajax.php?jsrandid=427&action=search&option=location&info=shanghai_FullTime&page=%d'

LIST_XPATH = '//*/table/tr'
TITLE_PATH = 'td[2]/a'
DATE_PATH = 'td[6]'

class YingJieShengCollecotr(collector.Collector):
    def pull(self):
        print "YingJieSheng pulling from topic collector!!"

    def clone(self):
        print "Start cloning from www.yingjiesheng.com..."
        parser = etree.HTMLParser(encoding='gbk')

        pages = range(1, 50)
        for page in pages:
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                #datetime.strptime - can you please work with unicode???
                time = node2.text.replace(u'年', '-').replace(u'月', '-').replace(u'日', '-')
                time = datetime.datetime.strptime(time, '%Y-%m-%d-')
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)