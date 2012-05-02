import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://bbs.fudan.edu.cn/bbs/tdoc?bid=431&start=%d'
LIST_XPATH = '//*/po'
BRD_XPATH = '//*/brd'
ITEM_URL = 'bbs.fudan.edu.cn/bbs/tcon?new=1&bid=431&f=%s'

QUERY_PAGES = 20

class FudanbbsCollecotor(collector.Collector):
    def fetch(self):
        parser = etree.HTMLParser(encoding='gbk')

        total = -1
        pages = range(0, QUERY_PAGES + 1)
        for page in pages:
            if not page:
                start_index = 0
            else:
                start_index = total - page * 20

            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            brd = tree.xpath(BRD_XPATH)
            total = int(brd[0].attrib['total'])

            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                title = node.text
                time = node.attrib['time']
                time = datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')
                url = ITEM_URL % node.attrib['id']
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)