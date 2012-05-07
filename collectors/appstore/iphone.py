#.-.coding=utf8

__author__ = 'xukaifang'


import urllib2
from lxml import etree
from kernel import collector
import datetime

FIRST_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-0-1-1/'
SECOND_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-0-1-2/'
LIST_URL='http://www.app111.com/all/1-0-0-0-0-0-1-%d/' # range from 1~999
LIST_XPATH='//*[@id="main_list_ul"]/li[position()>0]'
TITLE_PATH='div/div/div/div[2]/a'
DATE_PATH='div/div/div/div[3]/span[3]'

class IphoneCollector(collector.Collector):
    def fetch(self):
        parser = etree.HTMLParser(encoding='utf-8')
        print 'start fetching from app111.com'
        
        #pages=range(1,1000)
        pages=range(1,2)
        for page in pages:
            text=urllib2.urlopen(LIST_URL %page).read(-1)
            tree=etree.HTML(text, parser=parser)
            nodes=tree.xpath(LIST_XPATH)


            for node in nodes:
                try:
                    node1=node.find(TITLE_PATH)
                    title=node1.text.strip()
                    url=node1.attrib['href']
                    node2=node.find(DATE_PATH)
                    time=node2.text
                    time=time.replace(u'年','-')
                    time=time.replace(u'月','-')
                    time=time.replace(u'日','')
                    print "%s:%s - %s" %(time,title,url)
                    collector.object_found.send(self,time=time,title=title,url=url)
                except:
                    print time
            
