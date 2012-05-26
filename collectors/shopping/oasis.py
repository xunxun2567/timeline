# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.oasis-stores.com.cn/index.php?route=product/latest&page=%d'
XPATH = '//*/div[@class="product-list"]/div/dl'

class OasisCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Goelia started.')
        parser = etree .HTMLParser(encoding='utf-8')

        for page in range(1,7):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % page
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('dd/a/img')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['src']

                sub_node = node.find('dt/a')
                title = sub_node.text
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])

                price = self.getPrice(ourl)

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                leibie = u"女装"
                )

    def getPrice(self, url):
        parser = etree .HTMLParser(encoding='utf-8')
        text = urllib2.urlopen(url).read()
        tree = etree.HTML(text, parser=parser)

        nodes = tree.xpath('//*[@id="tabs"]/span')
        for node in nodes:
            #print etree.tostring(node, method='html', encoding='utf-8')
            price = node.text
            #print price
            price = price[len(u"售价："):len(price)]
        return price