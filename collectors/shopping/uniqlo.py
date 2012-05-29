# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.uniqlo.cn/search.htm?search=y&scid=%s&viewType=grid&orderType=_hotsell&pageNum=%d#anchor'
XPATH = '//*/ul[@class="shop-list"]/li/div[1]'

class UniqloCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Uniqlo started.')
        self.getData('138188203', 3, u'男装')    #男装
        self.getData('138188209',3, u'女装')     #女装
        self.getData('411880248',3,u'童装')     #孩童
        self.getData('237719246',3, u'婴儿')     #婴儿

    def getData(self, category, pages, leibie):
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
                price =   u'￥' + price[0: price.index('.')]

                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                leibie = leibie
                )