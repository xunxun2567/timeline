# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.crocs.cn/showcase.php?filter_type=%s&filter_segment=%s&filter_color=\
&filter_size=&filter_price=&filter_use=&filter_lifestyle=&product_sort=&product_page=%d'
XPATH = '//*[@id="content"]/table[2]/tr/td/table'

class CrocsCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Crocs started.')
        self.getData('w', 'shoes',10, u'女鞋')
        self.getData('m', 'shoes',6, u'男鞋')
        self.getData('m-w','shoes',3, u'男鞋-女鞋')
        self.getData('k', 'shoes',7, u'童鞋')
        self.getData('','accessories',14,u'配件')

    def getData(self, category, subcate, pages, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s-%s:' % (category, subcate))
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % (subcate, category, page)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            nodes = tree.xpath(XPATH)
            time = datetime.datetime.now().strftime('%Y-%m-%d')
            for node in nodes:
                #print etree.tostring(node, method='html', encoding='utf-8')
                sub_node = node.find('tr[2]/td/b/b/font')
                if sub_node is None:
                    print u"非新款"
                    continue

                sub_node = node.find('tr[1]/td/a')
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])
                image_url = sub_node.find('img').attrib['src']

                sub_node = node.find('tr[3]/td/b')
                title = sub_node.text

                sub_node = node.find('tr[4]/td')
                price = sub_node.text.strip()
                price = u'￥' + price[len('RMB ' ): price.index('.')]

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                leibie = leibie
                )