# .-. coding=utf-8
import urllib2
import datetime
import json
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://china.coach.com/online/handbags/-%s-14001-14500-5000000000000080060-cn?t1Id=5000000000000079052&t2Id=5000000000000080060&tier=2&LOC=LN'
PRODUCT_URL = 'http://china.coach.com/online/handbags/ProductShortDescriptionJSONView?storeId=14001&catalogId=14500&langId=-7&productIds='
XPATH = '//*[@id="layout"]/div[@class="oneByOne gwt_product"]'

class CoachCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Coach started.')
        self.getData('coachnews_all_new')   #女包
       # self.getData('men_newarrivals')     #男包

    def getPrice(self, pid):
        url = PRODUCT_URL + pid
        text = urllib2.urlopen(url).read()
        data = json.loads(text,encoding='utf-8')
        info = data["products"]
        return info[0]["unitPrice"]

    def getData(self, category):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s:' % category)
        url = LIST_URL % category
        text = urllib2.urlopen(url).read()
        tree = etree.HTML(text, parser=parser)

        time = datetime.datetime.now().strftime('%Y-%m-%d')
        nodes = tree.xpath(XPATH)
        for node in nodes:
            #sub_node = node.find('a[1]')
            #ourl = urlparse.urljoin(url,sub_node.attrib['href'])

            sub_node = node.find('a[1]/img')
            #print etree.tostring(node, method='html', encoding='utf-8')
            image_url = sub_node.attrib['src']
            title = sub_node.attrib['alt']
            productinfo = sub_node.attrib['onmouseover']
            productID = productinfo[productinfo.index("('")+2:productinfo.index("',")]
            price = self.getPrice(productID)

            #self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
            self.logger.info('%s(%s) - %s' % (title, price, image_url))
            collector.object_found.send(
            self,
            time = time, title = title, url = image_url,
            image_url = image_url,
            #price = price,
            )