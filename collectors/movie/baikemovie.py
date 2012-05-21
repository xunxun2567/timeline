# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL= 'http://baike.baidu.com/wiki_1-0/list-php/dispose/taglist.php?tag=%B5%E7%D3%B0&offset='
LIST_XPATH = '//*[@id="content"]/table'
TITLE_PATH = 'tr/td/font/a'
DATE_PATH = 'tr/td/font[2]/span'

class BaikeMovieCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info("Start fetching from baike.baidu.com...")
        parser = etree.HTMLParser(encoding='gb18030')
        pages = range(0, 77)
        for page in pages:
            self.logger.info(page)
            text = urllib2.urlopen(LIST_URL + (page * 10).__str__()).read(-1)
            index1 = text.find('<!--')
            while index1 > 0 :
                text = text[0:index1] +  text[text.index('-->')+3:len(text)]
                index1 = text.find('<!--')
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)

            for node in nodes:
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                timetext = node2.text
                time = timetext[timetext.index(u"字") + 2:len(timetext)]
                self.logger.info(u"%s: %s - %s" % (time, title, url))
                collector.object_found.send(self, time=time, title=title, url=url)
