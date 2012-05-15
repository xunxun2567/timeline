#coding=utf-8

import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL= 'http://movie.youku.com/search/index/_page40487_%d_cmodid_40487'
LIST_XPATH = '//*[@id="m13055109992"]/div[1]/div/ul/li[1]/a'

LIST_URL_TV= 'http://tv.youku.com/search/index/_page40177_%d_cmodid_40177'
LIST_XPATH_TV = '//*[@id="m13050845531"]/div[1]/div/ul/li[1]/a'

class YoukuMovieCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching from movie.youku.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='utf-8')
        pages = range(1, 35)
        for page in pages:
            print page
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)

            for node in nodes:
                title = node.attrib['title']
                url = node.attrib['href']
                print u"%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)

class YoukuTVCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching from tv.youku.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='utf-8')
        pages = range(1, 35)
        for page in pages:
            print page
            text = urllib2.urlopen(LIST_URL_TV % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH_TV)

            for node in nodes:
                title = node.attrib['title']
                url = node.attrib['href']
                #print etree.tostring(node, method='html', encoding='utf-8')
                #print u"%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)