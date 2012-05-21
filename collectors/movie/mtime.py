# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://theater.mtime.com/China_Shanghai/movie/#hotplay'
LIST_XPATH = '//*[@id="hotplayRegion"]/li'
TITLE_PATH = 'div/div/div/div/a[2]'

class MtimeCollecotr(collector.BaseCollector):
    def fetch(self):
        self.logger.info("Start fetching from www.mtime.com...")
        parser = etree.HTMLParser(encoding='utf-8')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)

        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        nodes = tree.xpath(LIST_XPATH)
        for node in nodes:
            node1 = node.find(TITLE_PATH)
            title = node1.attrib['title']
            url = node1.attrib['href']
            self.logger.info("%s: %s - %s" % (time, title, url))
            collector.object_found.send(self, time=time, title=title, url=url)

