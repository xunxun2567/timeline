# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://shop.mango.com/CN/page/mango/%E6%9C%80%E6%96%B0%E6%AC%BE/?n='
XPATH = '//*[@id="iteradorPrendas"]/tr/td/table'

class MangoCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('MANGO started.')

        parser = etree .HTMLParser(encoding='utf-8')
        for page in range(1,4):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL + page.__str__()
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('tr[1]/td/div/a/img')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['src']

                sub_node = node.find('tr[1]/td/div/img')
                image_url_backup = sub_node.attrib['src']

                sub_node = node.find('tr[2]/td/div/table/tr[2]/td/a')
                title = sub_node.find('span').text
                url = urlparse.urljoin("http://shop.mango.com/",sub_node.attrib['href'])

                sub_node = node.find('tr[2]/td/div/table/tr[3]/td/span')
                price = sub_node.text

                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                )