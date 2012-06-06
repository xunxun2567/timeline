# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector
from kernel.collector import object_found

LIST_URL = 'http://www.amazon.cn/%E4%BF%83%E9%94%80-%E7%89%B9%E4%BB%B7/b/ref=cs_top_nav_gb27/475-8883503-9352433?ie=UTF8&node=42450071'
LIST_XPATH = '//*[@id="hot"]/div[1]/div[2]/ul/li'
TITLE_PATH = 'div[2]/a'
PREVIEW_PATH = 'div[1]/a/img'
PRICE_PATH = 'div[3]/strong'

class AmazonCollecotr(collector.BaseCollector):
    def fetch(self):
        self.logger.info("Start fetching data from www.360buy.com...")
        parser = etree.HTMLParser(encoding='gbk')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)

        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        nodes = tree.xpath(LIST_XPATH)
        for node in nodes:
            node1 = node.find(TITLE_PATH)
            #print  etree.tostring(node, method='html', encoding='utf-8')
            title = node1.attrib['title']
            url = node1.attrib['href']
            node2 = node.find(PREVIEW_PATH)
            preview = node2.attrib['src']
            node3 = node.find(PRICE_PATH)
            price = node3.text
            self.logger.info("%s: %s - %s" % (time, title, url))
            self.logger.info("%s - %s" % (price, preview))
            object_found.send(self, time=time, title=title, url=url, preview=preview ,price=price)