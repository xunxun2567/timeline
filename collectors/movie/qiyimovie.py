# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL= 'http://list.iqiyi.com/www/1/----------0--2-1-%d-1---.html'
LIST_XPATH = '/html/body/div[3]/div[4]/div[2]/div[2]/div[2]/div[2]/ul/li/a[2]'

class QiyiMovieCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching from www.qiyi.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='utf-8')
        pages = range(1, 80)
        for page in pages:
            print page
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)

            for node in nodes:
                #print etree.tostring(node, method='html', encoding='utf-8')
                title = node.text
                url = node.attrib['href']
                print u"%s: %s - %s" % (time, title, url)
                #collector.object_found.send(self, time=time, title=title, url=url)
