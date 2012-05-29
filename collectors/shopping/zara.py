# .-. coding=utf-8
import urllib2
import datetime
import json
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.zara.com/webapp/wcs/stores/servlet/category/cn/zh/zara-S%s/%s'
XPATH = '//*/div[@class="main"]/div[@class="body"]/script'

class ZaraCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Zara started.')
        self.getData('199002/%E5%A5%B3%E5%A3%AB', 2, u'女装')
        self.getData('199003/TRF',2, u'女装')
        self.getData('199004/%E7%94%B7%E5%A3%AB',2, u'男装')
        self.getData('199005/%E5%A5%B3%E7%AB%A5',2, u'童装')
        self.getData('199006/%E7%94%B7%E7%AB%A5',2, u'童装')
        self.getData('199007/%E5%A5%B3%E5%A9%B4',2, u'婴儿')
        self.getData('199008/%E7%94%B7%E5%A9%B4',2, u'婴儿')
        self.getData('199009/%E8%BF%B7%E4%BD%A0',2, u'婴儿')

    def getData(self, category, pages, leibie):
        parser = etree .HTMLParser(encoding='utf-8')
        time = datetime.datetime.now().strftime('%Y-%m-%d')
        year = datetime.datetime.now().year
        self.logger.info('Category: %s:' % category)
        for page in range(1,pages):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL %(year, category)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            nodes = tree.xpath(XPATH)
            productText = nodes[0].text
            productText = productText[productText.index("categoryData: ") + len("categoryData: ") :productText.rindex('},' )+1]
            data = json.loads(productText)
            urlPrefix = data["urlPrefix"]
            imgPrefix = data["imgPrefix"]
            items = data["items"]
            for item in items:
                title = item["name"]
                price = item["numPrice"]
                if price > 0:
                    price = u'￥' + price.__str__()
                url = urlPrefix + item["link"]["full"]
                image_url = imgPrefix + item["image"]["standard"]
                self.logger.info('%s (%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = url,
                image_url = image_url,
                price = price,
                leibie = leibie
                )