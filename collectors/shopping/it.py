# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.itezhop.com/ezhop/ezhop/product/productlist.do?gender=%s&status=NEW_IN&pageno=%d&'
XPATH = '//*/div[@class="productList"]/ul/li/table/tbody'

class ITCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('I.T. started.')
        self.getData('F',7)
        self.getData('M',9)

    def getData(self, category, pages):
        parser = etree .HTMLParser(encoding='utf-8')
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL % (category, page)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                #print etree.tostring(node, method='html', encoding='utf-8')
                sub_node = node.find('tr[2]/td[1]/div[@class="listInfo"]/ul')
                sub_node1 = sub_node.find('li[1]/a')
                sub_node2 = sub_node.find('li[2]/a')
                title = sub_node1.text + ' ' + sub_node2.text

                sub_node = node.find('tr[3]/td[1]/div[1]/span[@class="proPrice"]')
                price_text = etree.tostring(sub_node, method='html', encoding='utf-8')
                price_num = price_text[price_text.index('</span>') + len('</span>'):price_text.rindex('</span>')]
                price = sub_node.find('span').text + price_num

                sub_node = node.find('tr[1]/td[1]/div[1]/div[@class="photo"]/a')
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])

                sub_node = sub_node.find('img')
                image_url = urlparse.urljoin(url,sub_node.attrib['src'])

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                )