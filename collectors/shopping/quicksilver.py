# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.quiksilver.cn/cn/tw/productlist.php?pid=%s&sid=%d'
XPATH = '/html/body/div[2]/div/div[2]/div/div[2]/table/tr/td[2]/table/tr/td/table/tr/td/table'

class QuicksilverCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Quicksilver started.')
        self.getData('10',76,81, u'男装')     #男服装
        self.getData('3',72,76, u'男式配件')      #男配件
        self.getData('19',69,72, u'男装')     #男裤子

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