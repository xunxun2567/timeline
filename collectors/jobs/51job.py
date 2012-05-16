import urllib2
from lxml import etree
from kernel import collector

LIST_URL = 'http://search.51job.com/jobsearch/search_result.php?fromJs=1&lang=c&stype=1&postchannel=0000&fromType=1&line=&confirmdate=9&keywordtype=0&keyword=&curr_page=%d&jobarea=0200&funtype=0000&industrytype=00'

LIST_XPATH = '/html/body/div[2]/div[5]/div[3]/div[2]/table/tr[@class="tr0"]'
TITLE_PATH = 'td[2]/a'
DATE_PATH = 'td[5]/span'

class WWW51JobCollector(collector.BaseCollector):
    def fetch(self):
        parser = etree.HTMLParser(encoding='gbk')

        pages = range(1, 1000)
        for page in pages:
            text = urllib2.urlopen(LIST_URL % page).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                time = node2.text
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)