# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.zara.com/webapp/wcs/stores/servlet/category/cn/en/zara-S%s%s'
XPATH = '//*/ul[@class="shop-list"]/li/div[1]'

class ZaraCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Zara` started.')
        self.getData('138188203', 3)    #男装
        self.getData('138188209',3)     #女装
        self.getData('411880248',3)     #孩童
        self.getData('237719246',3)     #婴儿

    def getData(self, category, pages):
        parser = etree .HTMLParser(encoding='gbk')
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL %(category, page)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                #print etree.tostring(node, method='html', encoding='utf-8')
                sub_node = node.find('div[1]/a')
                url = sub_node.attrib['href']

                sub_node = sub_node.find('img')
                #print etree.tostring(sub_node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['data-ks-lazyload']

                sub_node = node.find('div[2]/a')
                title = sub_node.text

                sub_node = node.find('div[3]/strong')
                price = sub_node.text.strip()

                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                )