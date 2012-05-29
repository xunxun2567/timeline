# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.roxy.cn/cn/tw/productlist.php?pid=%s&sid=%d'
XPATH = '/html/body/div/div/table[2]/tr/td/table/tr/td/table/tr/td/table'

class RoxyCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Roxy started.')
        self.getData('10',89,95, u'女装')     #女服装
        self.getData('3',84,89, u'女式配件')  #女配件
        self.getData('21',81,84, u'女装')     #女裤子

    def getData(self, category, start,end, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        for subcate in range(start, end):
            self.logger.info('category: %s-%d:' % (category,subcate))
            url = LIST_URL % (category,subcate)
            for page in range(0, 10):
                self.logger.info('Page: %d:' % (page+1))
                data = "start=%d" % (page * 8)
                text = urllib2.urlopen(url, data).read()
                tree = etree.HTML(text, parser=parser)

                time = datetime.datetime.now().strftime('%Y-%m-%d')
                nodes = tree.xpath(XPATH)
                for node in nodes:
                    sub_node = node.find('tr[1]/td/a')
                    #print etree.tostring(node, method='html', encoding='utf-8')
                    ourltext = sub_node.attrib['onclick']
                    ourl = urlparse.urljoin(url,ourltext[ourltext.index(".."):ourltext.rindex("'")])
                    image_url = urlparse.urljoin(url,sub_node.find('img').attrib['src'])

                    sub_node = node.find('tr[2]/td/div')
                    title = sub_node.text

                    sub_node = node.find('tr[3]/td/div')
                    pricetext =  etree.tostring(sub_node, method='html', encoding='utf-8')
                    price =  u'￥' + pricetext[pricetext.index("RMB") + len("RMB"):pricetext.index("</div>")]

                    self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                    collector.object_found.send(
                    self,
                    time = time, title = title, url = ourl,
                    image_url = image_url,
                    price = price,
                    leibie = leibie
                    )