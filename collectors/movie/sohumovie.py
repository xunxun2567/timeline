# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL= 'http://tv.sohu.com/movieall/'
LIST_XPATH = '/html/body/center/div[5]/dl/dd/ul/li/a'

LIST_URL_TV= 'http://tv.sohu.com/tvall/'

class SohuMovieCollector(collector.Collector):
    def fetch(self):
        print "Start fetching movie from tv.sohu.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='gbk')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)
        nodes = tree.xpath(LIST_XPATH)

        for node in nodes:
            title = node.text
            url = node.attrib['href']
            print u"%s: %s - %s" % (time, title, url)
            collector.object_found.send(self, time=time, title=title, url=url)

class SohuTVCollector(collector.Collector):
    def fetch(self):
        print "Start fetching tv from tv.sohu.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='gbk')
        text = urllib2.urlopen(LIST_URL_TV).read(-1)
        tree = etree.HTML(text, parser=parser)
        nodes = tree.xpath(LIST_XPATH)

        for node in nodes:
            title = node.text
            url = node.attrib['href']
            print u"%s: %s - %s" % (time, title, url)
            collector.object_found.send(self, time=time, title=title, url=url)
