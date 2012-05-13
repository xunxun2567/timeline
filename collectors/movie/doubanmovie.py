# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://movie.douban.com/'
LIST_XPATH = '/html/body/div[2]/div[2]/div/div/div[4]/ul/li'
TITLE_PATH = 'div[2]/h3/a'

LIST_URL_TV = 'http://movie.douban.com/tv/'
LIST_XPATH_TV = '/html/body/div[2]/div[2]/div/div/div[4]/table/tr/td/a'
#TITLE_PATH_TV = 'div[2]/h3/a'

class DoubanMovieCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching movies from www.douban.com..."
        parser = etree.HTMLParser(encoding='utf-8')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)

        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        nodes = tree.xpath(LIST_XPATH)
        for node in nodes:
            node1 = node.find(TITLE_PATH)
            title = node1.text
            url = node1.attrib['href']
            print "%s: %s - %s" % (time, title, url)
            #collector.object_found.send(self, time=time, title=title, url=url)

class DoubanTVCollecotr(collector.Collector):
        def fetch(self):
            print "Start fetching tv from www.douban.com..."
            parser = etree.HTMLParser(encoding='utf-8')
            text = urllib2.urlopen(LIST_URL_TV).read(-1)
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().date().strftime('%Y-%m-%d')
            nodes = tree.xpath(LIST_XPATH_TV)
            for node in nodes:
                title = node.attrib['title']
                url = node.attrib['href']
                print "%s: %s - %s" % (time, title, url)
                #collector.object_found.send(self, time=time, title=title, url=url)