# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.esprit.cn/c/%s%d/newBrand.htm?sp=1'
XPATH = '//*/div[@class="sku_list"]/ul/li'

class EspritCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Eesprit started.')
        self.getData('0-0-1-',2,3)      #etc
        self.getData('2-5-3-',11,21)    #女装
        self.getData('3-7-3-',25,33)    #男装
        self.getData('2-6-3-',21,25)    #女配
        self.getData('3-8-3-',33,37)    #男配
        self.getData('4-9-3-',37,39)    #童上装
        self.getData('4-10-3-',39,41)    #童下装

    def getData(self, category, start,end):
        parser = etree .HTMLParser(encoding='utf-8')
        for subcate in range(start, end):
            self.logger.info('category: %s%d:' % (category,subcate))
            url = LIST_URL % (category,subcate)
            if category == '0-0-1-':
                url += '&lable=EDC'
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[@class="sku_pic"]')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = urlparse.urljoin(url,sub_node.find('a[1]/img').attrib['src'])
                image_url_backup = urlparse.urljoin(url,sub_node.find('a[2]/img').attrib['src'])

                sub_node = node.find('div[@class="sku_title grey2"]/a')
                title = sub_node.find('span').text
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])

                sub_node = node.find('div[@class="sku_price"]/a/span')
                price = sub_node.text

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                )