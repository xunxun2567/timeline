# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.360buy.com/'
LIST_XPATH = '//*[@id="hot"]/div[1]/div[2]/ul/li'
TITLE_PATH = 'div[2]/a'
PREVIEW_PATH = 'div[1]/a/img'
PRICE_PATH = 'div[3]/strong'

class JingdongCollecotr(collector.BaseCollector):
    def fetch(self):
        print "Start fetching data from www.360buy.com..."
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
            print "%s: %s - %s" % (time, title, url)
            print "%s - %s" % (price, preview)
            #collector.object_found.send(self, time=time, title=title, url=url, preview=preview ,price=price)