import datetime
from lxml import etree
from kernel import collector

LIST_URL_B = 'http://www.baidu.com/'
LIST_XPATH_B = '//*[@id="lg"]'
URL_PATH_B = 'img'
TITLE_PATH_B ='map/area'

LIST_URL_G = 'http://www.google.com/'
LIST_XPATH_G = '//*[@id="hplogo"]'
URL_PATH_G = 'img'

class BaiduLogoCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info("Start cloning logo url from baidu.com...")
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='gb2312')
        text = urllib2.urlopen(LIST_URL_B).read(-1)
        tree = etree.HTML(text, parser=parser)

        nodes = tree.xpath(LIST_XPATH_B)
        for node in nodes:
            node1 = node.find(URL_PATH_B)
            url = node1.attrib['src']
            node2 = node.find(TITLE_PATH_B)
            title = node2.attrib['title']
            self.logger.info("%s: %s - %s" % (time, title, url))
            collector.object_found.send(self, time=time, title=title, url=url)

class GoogleLogoCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info("Start cloning logo url from google.com...")
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        parser = etree.HTMLParser(encoding='Big5')
        text = urllib2.urlopen('http://www.google.com').read(-1)
        #print text
        tree = etree.HTML(text, parser=parser)

        nodes = tree.xpath(LIST_XPATH_G)
        url=''
        for node in nodes:
            for attr in node.attrib:
                if attr == 'src':
                    url = node.attrib['src']
                    url = LIST_URL_G + url[1:len(url)-1]
                if attr == 'style':
                    url = node.attrib['style']
                    url = LIST_URL_G + url[len('background:url(/'):url.index(')')]
        title = node.attrib['title']
        self.logger.info("%s: %s - %s" % (time, title, url))
        collector.object_found.send(self, time=time, title=title, url=url)
