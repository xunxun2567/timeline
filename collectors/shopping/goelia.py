# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL1 = 'http://mall.goelia.com.cn/index.php/gallery-index---1--%d-82-grid.html?'
LIST_URL2 = 'scontent=b%2C_ANY__t%2C1_p%2C0'
XPATH = '//*[@id="gallery-grild-list"]/ul/li'

class GoeliaCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Goelia started.')
        parser = etree .HTMLParser(encoding='utf-8')

        for page in range(1,9):
            self.logger.info('Page: %d:' % page)
            url = LIST_URL1 % page + LIST_URL2
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[@class="goodpic"]/a/img')
                #print etree.tostring(node, method='html', encoding='utf-8')
                image_url = sub_node.attrib['src']

                sub_node = node.find('div[@class="goods-main"]/div[1]/h6/a')
                title = sub_node.text
                ourl = urlparse.urljoin(url,sub_node.attrib['href'])

                sub_node = node.find('div[@class="goods-main"]/div[2]/ul/li[1]/em[@class="sell-price"]')
                price = sub_node.text.strip()

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                )