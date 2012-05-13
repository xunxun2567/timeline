# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.gewara.com/movie/'
LIST_XPATH = '//*[@id="loadingTwitter"]/ul/li'
TITLE_PATH = 'div/a'
DATE_PATH = 'div[2]/div/div/div[2]/div/div/p[2]'

LIST_ALL_URL = 'http://www.gewara.com/movie/searchMovie.xhtml?pageNo=%d'
LIST_ALL_XPATH = '//*[@id="ui_layout"]/div/div/ul/li'
TITLE_ALL_PATH = 'div[2]/div/div/div[2]/div/div/a'
DATE_ALL_PATH = 'div[2]/div/div/div[2]/div/p/span'

class GewaraCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching from www.gewara.com..."
        parser = etree.HTMLParser(encoding='utf-8')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)

        nodes = tree.xpath(LIST_XPATH)
        for node in nodes:
            node1 = node.find(TITLE_PATH)
            title = node1.attrib['title']
            url = 'http://www.grwara.com'+ node1.attrib['href']
            node2 = node.find(DATE_PATH)
            timetext = etree.tostring(node2, method='html', encoding='utf-8')
            time = timetext[timetext.index('</em>') + len('</em>'):timetext.index('</p>')]
            print "%s: %s - %s" % (time, title, url)
            #collector.object_found.send(self, time=time, title=title, url=url)

class GewaraAllCollecotr(collector.Collector):
    def fetch(self):
        print "Start fetching all movies from www.gewara.com..."
        parser = etree.HTMLParser(encoding='utf-8')

        pages = range(0, 3)
        for page in pages:
            text = urllib2.urlopen(LIST_ALL_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_ALL_XPATH)

            for node in nodes:
                node1 = node.find(TITLE_ALL_PATH)
                if node1 is None:
                    continue
                title = node1.attrib['title']
                url = 'http://www.grwara.com'+ node1.attrib['href']
                nodes2 = node.find(DATE_ALL_PATH)
                for node2 in nodes2:
                    node3 = node.find(DATE_ALL_PATH + '/em')
                    if node3 is not None:
                        nodename = node3.text
                        if nodename == u'上映日期：':
                            timetext = etree.tostring(node2, method='html', encoding='utf-8')
                            time = timetext[timetext.index('</em>') + len('</em>'):len(timetext)]
                            if time != '':
                                print "%s: %s - %s" % (time, title, url)
                                #collector.object_found.send(self, time=time, title=title, url=url)