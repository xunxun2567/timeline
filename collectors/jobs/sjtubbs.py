import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'https://bbs.sjtu.edu.cn/bbstdoc,board,JobInfo,page,%d.html'

LIST_XPATH = '//*/table/tr[position()>1]'
TITLE_PATH = 'td[5]/a'
DATE_PATH = 'td[4]'

class SJTUbbsCollecotr(collector.Collector):
    def fetch(self):
        parser = etree.HTMLParser(encoding='gbk')

        pages = range(2950, 3050)
        for page in pages:
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                try:
                    node1 = node.find(TITLE_PATH)
                    title = node1.text
                    url = node1.attrib['href']
                    node2 = node.find(DATE_PATH)
                    time = node2.text
                    time = datetime.datetime.strptime(time, '%b  %d %H:%M')
                    time = datetime.datetime(year=2012, month=time.month, day=time.day)
                    print "%s: %s - %s" % (time, title, url)
                    collector.object_found.send(self, time=time, title=title, url=url)
                except:
                    pass
