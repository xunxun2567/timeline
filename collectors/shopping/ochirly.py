# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.ochirly.com/webapp/wcs/stores/servlet/AjaxCatalogSearchResultView?searchTermScope=&searchType=0\
&filterTerm=&orderBy=&maxPrice=&showResultsPage=true&langId=-7&sType=SimpleSearch&metaData=&pageSize=28&manufacturer=&\
resultCatEntryType=&catalogId=11051&pageView=image&searchTerm=&minPrice=&categoryId=245004&storeId=10151&beginIndex=%d'
XPATH = '//*/div[@class="listDiv goodsList"]/table/tr/td/ul/li'

class OchirlyCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Ochirly started.')
        parser = etree .HTMLParser(encoding='gbk')

        for page in range(0,21):
            self.logger.info('Page: %d:' % (page+1))
            url = LIST_URL % (page * 28)
            text = urllib2.urlopen(url).read()
            tree = etree.HTML(text, parser=parser)

            data = {
                'a': '123',
            }

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                #print etree.tostring(node, method='html', encoding='utf-8')
                sub_node = node.find('div[1]/div[1]/a[1]/img')
                image_url = sub_node.attrib['src']

                sub_node = node.find('div[2]/a')
                title = sub_node.find('div').text
                ourl = sub_node.attrib['href']

                sub_node = node.find('div[2]/div[1]/span[@class="price bold"]')
                price = sub_node.text.strip()

                self.logger.info('%s(%s) - %s @ %s' % (title, price, ourl, image_url))
                collector.object_found.send(
                self,
                time = time, title = title, url = ourl,
                image_url = image_url,
                price = price,
                )