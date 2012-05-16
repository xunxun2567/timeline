# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

#LIST_URL = 'http://www.vancl.com/'
#LIST_XPATH = '//*[@id="play_list"]/div[1]/a/img'
##TITLE_PATH = 'div[2]/h3/a'
#
#class VanclCollecotr(collector.BaseCollector):
#    def fetch(self):
#        print "Start fetching ads from www.vancl.com..."
#        parser = etree.HTMLParser(encoding='utf-8')
#        text = urllib2.urlopen(LIST_URL).read(-1)
#        tree = etree.HTML(text, parser=parser)
#
#        time = datetime.datetime.now().strftime('%Y-%m-%d')
#        nodes = tree.xpath(LIST_XPATH)
#        for node in nodes:
#            #node1 = node.find(TITLE_PATH)
#            #print  etree.tostring(node, method='html', encoding='utf-8')
#            title = node.attrib['alt']
#            url = node.attrib['originalsrc']
#            print "%s: %s - %s" % (time, title, url)
#            collector.object_found.send(self, time=time, title=title, url=url)

#BASE_URL = 'http://s.vancl.com/%s.html?s=1'
BASE_URL = 'http://s.vancl.com/search?p=%d&s=1'
XPATH = '//*/div[@id="vanclproducts"]/ul/li'

class VanclCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Vancl started.')
        parser = etree .HTMLParser(encoding='utf-8')
        for page in range(1, 100):
            self.logger.info('Page: %d:' % page)
            text = urllib2.urlopen(BASE_URL % page).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[1]/a')
                title = sub_node.attrib['title']
                url = sub_node.attrib['href']
                image_url = sub_node.find('img').attrib['original']
                sub_node = node.find('div[2]/span[2]')
                price = sub_node.text
                self.logger.info('%s(%s) - %s @ %s' % (title, price, url, image_url))
                collector.object_found.send(
                    self,
                    time = time, title = title, url = url,
                    image_url = image_url,
                    price = price,
                )