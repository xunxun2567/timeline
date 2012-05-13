# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL= 'http://movie.tudou.com/albumtop/c22t-1v-1z-1a-1y-1h-1s1p%d.html'
LIST_XPATH = '//*[@id="mainCol"]/div[2]/div/div/div[2]/h6/a'

class TudouMovieCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching from movie.tudou.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='gbk')
        pages = range(1, 31)
        for page in pages:
            print page
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            #print text
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)

            for node in nodes:
                title = node.text
                url = node.attrib['href']
                print u"%s: %s - %s" % (time, title, url)
                #collector.object_found.send(self, time=time, title=title, url=url)
