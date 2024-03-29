# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.c-and-a.com.cn/cn/fashion/product/index.php?page=%d&gender=%s'
XPATH = '/html/body/div[3]/div[2]/div[4]/div/div[1]'

class CACollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('C&A started.')
        self.getData('female', 14, u"女装")
        self.getData('male',12, u"男装")
        self.getData('kids',6, u"童装")
        self.getData('accessory',5, u"配件")

    def getData(self, category, pages, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL %(page, category)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('a[1]/img')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = urlparse.urljoin(url,sub_node.attrib['src'])

                sub_node = node.find('div[1]/div[1]/a')
                title = sub_node.text
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])

                sub_node = node.find('div[1]/div[2]')
                price = sub_node.text.strip()
                price = u'￥' + price[0:price.index(' RMB')]

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                leibie = leibie
                )