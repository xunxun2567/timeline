# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.hm.com/cn/subdepartment/%s?Nr=90001#page=%d&Nr=90001'
XPATH = '//*/ul[@id="list-products"]/li/div'

class HMCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('H&M started.')
        self.getData('ladies',8)
        self.getData('men',2)
        self.getData('kids',4)

    def getData(self, category, pages):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            text = urllib2.urlopen(LIST_URL %(category, page)).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('a[1]')
                title = sub_node.attrib['title']
                url = sub_node.attrib['href']
                price = sub_node.find('span/span/span').text

                sub_node = node.find('div[1]')
                image_url = sub_node.find('img[2]').attrib['src']
                #image_url_backup = sub_node.find('img[1]').attrib['src']

                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                )