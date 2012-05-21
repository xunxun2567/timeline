#.-.coding=utf8

__author__ = 'wangguodong'

import urllib2
import urlparse
from kernel import collector
from lxml import etree
from kernel.collector import object_found

URL_PATTERN = 'http://weiqi.sports.tom.com/php/listqipu%s.html'
LIST_XPATH='/html/body/div[4]/div[2]/ul[position()>1]'
URL_ITEM_PATTERN = 'http://weiqi.sports.tom.com/php/listqipu%s_%02d.html'
FETCHED_YEARS = ('', '2011', '2010', '2009', '2008', '2007', '2006', '2005', '2000')

class WeiqiCollector(collector.BaseCollector):

    def fetch(self):
        for year in FETCHED_YEARS:
            url = URL_PATTERN % year
            objects_in_year = self._get_objects_from_url(url)
#            result.extend(objects_in_year)
#            print "Year: %s, Retrieved: %d objects." % (year, len(objects))
#            print " " * 45 + "Total: %d" % len(result)
            page = 2
            while True:
                url = URL_ITEM_PATTERN % (year, page)
                objects_in_page = self._get_objects_from_url(url)
                if len(objects_in_page) == 0: break;

                page = page + 1


    def update(self):
        print "updating objects from weiqi.sports.tom.com..."

        return self.fetch()


    def _get_objects_from_url(self, url):
        objects = []
        parser = etree.HTMLParser(encoding='gbk')
        text = urllib2.urlopen(url).read(-1)
        tree = etree.HTML(text, parser=parser)
        nodes = tree.xpath(LIST_XPATH)

        for node in nodes:
            try:
                title_node = node.find('li[1]/a')
                time_node = node.find('li[2]')
                url_node = node.find('li[3]/a')
                if url_node == None: continue

                new_url = urlparse.urljoin(url, url_node.attrib['href']).replace('../', '')
                text = urllib2.urlopen(new_url).read(-1)

                time = time_node.text
                time=time.replace(u'年','-')
                time=time.replace(u'月','-')
                time=time.replace(u'日','')

                title = title_node.text
                title_parts = title.split(' ')
                contest = title_parts[0]
                contest_info = title_parts[1]

                object_got = {
                    'time': time,
                    'title': title,
                    'url': new_url,
                    }

                print "        Object retrieved: %s" % object_got['title']
                self.logger.info("%s: %s - %s" % (object_got, title, new_url))

                objects.append(object_got)
                object_found.send(self, time=time, title=title, url=new_url, check=True, contest=contest, info=contest_info, qipu=text)

            except:
                pass

        return objects