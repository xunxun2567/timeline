# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.gap.cn/new-arrivals/%s.html'
XPATH = '//*[@id="product-listing-results"]/div[position()<last()]/ul/li'

class GapCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('GAP started.')
        self.getData('men', 2)
        self.getData('women',2)
        self.getData('boys',2)
        self.getData('girls',2)
        self.getData('baby-boys',2)
        self.getData('baby-girls',2)

    def getData(self, category, pages):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % category
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('h5/a')
                #print etree.tostring(node, method='html', encoding='utf-8')
                url = sub_node.attrib['href']
                title = sub_node.text

                sub_node = node.find('div[3]/p/span/span')
                price = sub_node.text

                sub_node = node.find('div[1]/p/a/img')
                image_url = sub_node.attrib['src']

                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                )