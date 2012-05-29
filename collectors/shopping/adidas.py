# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.adidas.com/cn/catalogue/%s/%s/?p=%d'
XPATH = '//*/div[@class="cards"]'

class AdidasCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Adidas started.')
        self.getData('men', 'shoes',7, u"男鞋")
        self.getData('men', 'clothing',12, u"男装")
        self.getData('women', 'shoes',4, u"女鞋")
        self.getData('women','clothing',13, u"女装")
        self.getData('kids','shoes',2, u"童鞋")
        self.getData('kids','clothing',2, u"童装")

    def getData(self, category, subcate, pages, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s-%s:' % (category, subcate))
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % (subcate, category, page)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[1]/a/img')
                image_url = sub_node.attrib['src']

                sub_node = node.find('div[3]/a')
                #print etree.tostring(node, method='html', encoding='utf-8')
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])
                title = sub_node.text

                price = '0'

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                leibie = leibie
                )