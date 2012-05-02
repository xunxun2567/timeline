import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL_PART1 = 'http://myresume.zhaopin.com/jobs/request.asp?PublishDate=&industry=&JobLocation=538&sortby=&JobProvince=%E5%85%A8%E5%9B%BD&SchJobType=&subJobType=&totalpage=79&vip_type=&sButton=P%3A'
LIST_URL_PART2 = '&ql=&key_id=&suuid=4383_40961.94&position_name=&KeyWord='

LIST_XPATH = '//*/form/table/tr[position()>2]'
TITLE_PATH = 'td[2]/a'
DATE_PATH = 'td[4]'

class ZhaopinCollecotr(collector.Collector):
    def fetch(self):
        parser = etree.HTMLParser(encoding='utf8')

        pages = range(1, 40)
        for page in pages:
            text = urllib2.urlopen(LIST_URL_PART1 + page.__str__() + LIST_URL_PART2).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                if node.attrib['class'] == 'turnpage': break
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                time = datetime.datetime.strptime(node2.text, "%y-%m-%d")
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)