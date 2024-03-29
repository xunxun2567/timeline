# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.nikestore.com.cn/zone/001/list.htm?pn=%d&sort=&c1=%s&c2=%s&c3=&c4='
XPATH = '//*[@id="list-display-box"]/dl[@class="list-box"]'

class NikeCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Nike started.')
        self.getData('man', 'shoe',3, u'男鞋')
        self.getData('man', 'apparel',3, u'男装')
        self.getData('man','equipment',3, u'男式配件')
        self.getData('woman', 'shoe',3, u'女鞋')
        self.getData('woman','apparel',3, u'女装')
        self.getData('woman','equipment',3, u'女士配件')

    def getData(self, category, subcate, pages, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s-%s:' % (category, subcate))
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % (page, subcate, category)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('dt[@class="skuname"]/a')
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])
                title = sub_node.text

                sub_node = node.find('dt[@class="price"]/span[@id="listPrice"]')
                price = u'￥' + sub_node.text

                sub_node = node.find('dt[@class="img"]/a/img')
                #print etree.tostring(sub_node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['lazy_src']

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                leibie = leibie
                )