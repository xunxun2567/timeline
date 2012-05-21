# .-. coding=utf-8
import urllib2
import datetime
import urlparse
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.forever21.cn/Product/NewArrivals.aspx?category=forever21_all'
           #'http://www.forever21.cn/Product/NewArrivals.aspx?category=girls_app'
XPATH_1 = '/html/body/center/form/table/tr/td[2]/table/tr/td[2]/table[2]/tr/td/center/table/tr[2]/td/table/tr[3]/td/table[3]/td/table'
XPATH_2 = '/html/body/center/form/table/tr/td[2]/table/tr/td[2]/table[2]/tr/td/center/table/tr[2]/td/table/tr[3]/td/table[3]/tr/td/table'

class Forever21Collector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Forever21 started.')
        parser = etree .HTMLParser(encoding='utf-8')

        text = urllib2.urlopen(LIST_URL).read()
        #index1 = text.find('<!--')
        #while index1 > 0 :
        #    text = text[0:index1] +  text[text.index('-->')+3:len(text)]
        #    index1 = text.find('<!--')
        #print text
        tree = etree.HTML(text, parser=parser)

        time = datetime.datetime.now().strftime('%Y-%m-%d')
        nodes = tree.xpath(XPATH_1) + tree.xpath(XPATH_2)

        for node in nodes:
            #print etree.tostring(node, method='html', encoding='utf-8')
            sub_node = node.find('tr[@align="center"]/td/div/a/img')
            image_url = urlparse.urljoin(LIST_URL,sub_node.attrib['src'])

            sub_node = node.find('tr[@valign="top"]/td/a[last()]')
            title = sub_node.text
            url = urlparse.urljoin(LIST_URL,sub_node.attrib['href'])

            if 'men' in url:
                print "it belongs to men category"
            elif 'girls' in url or 'boys' in url:
                print "it belongs to kids category"
            sub_node = node.find('tr[@valign="top"]/td/font[@class="price"]')
            price = sub_node.text
            if price is None:
                price = sub_node.find('font').text

            self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
            collector.object_found.send(
            self,
            time = time, title = title, url = url,
            image_url = image_url,
            price = price,
            )