# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.etam.com.cn/chanpin/productsfilter/new/?___SID=U&ajax=true&cus_color=&cus_price=&id=2&limit=32&order=&p=%d&rand=48414'
XPATH = '//*/div[@class="category-products"]/div/ul/li'

class EtamCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Etam started.')
        parser = etree .HTMLParser(encoding='utf-8')

        for page in range(1,6):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % page
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[1]/a[2]/img')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['src']

                sub_node = node.find('h3/a')
                title = sub_node.text
                ourl = sub_node.attrib['href']

                sub_node = node.find('div[2]/p[1]/span[@class="price"]')
                if sub_node is None:
                    sub_node = node.find('div[2]/span/span[@class="price"]')
                price = sub_node.text.strip()

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                )