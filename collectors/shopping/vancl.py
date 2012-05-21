# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

BASE_URL = 'http://s.vancl.com/search?p=%d&s=1'
XPATH = '//*/div[@id="vanclproducts"]/ul/li'

class VanclCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Vancl started.')
        parser = etree .HTMLParser(encoding='utf-8')
        for page in range(1, 100):
            self.logger.info('Page: %d:' % page)
            text = urllib2.urlopen(BASE_URL % page).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[1]/a')
                title = sub_node.attrib['title']
                url = sub_node.attrib['href']
                image_url = sub_node.find('img').attrib['original']
                sub_node = node.find('div[2]/span[2]')
                price = sub_node.text
                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                    self,
                    time = time, title = title, url = url,
                    image_url = image_url,
                    price = price,
                )