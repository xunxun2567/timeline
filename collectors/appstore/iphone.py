#.-.coding=utf8

__author__ = 'xukaifang'


import urllib2
from lxml import etree
from kernel import collector
import datetime

FIRST_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-0-2-1/'
SECOND_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-0-2-2/'
THIRD_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-4-2-1/'
GAME_PAGE_URL='http://www.app111.com/all/1-0-0-0-0-6-0-2-1/'
LIST_URL='http://www.app111.com/all/1-0-0-0-0-6-0-2-%d/'
#LIST_URL='http://www.app111.com/all/1-0-0-0-0-0-2-%d/' # range from 1~999, sorted by time
LIST_CATEGORY_XPATH='/html/body/div[3]/ul/li[4]/p/a[position()>1]'
PAGE_NUM_XPATH='/html/body/div[4]/div[2]/span[2]'
LIST_XPATH='//*[@id="main_list_ul"]/li[position()>0]'
TITLE_PATH='div/div/div/div[2]/a'
DATE_PATH='div/div/div/div[3]/span[3]'


INCREMENT=3 #DEFINE THE PAGE TO BE VIEWED FOR INCREMENT

class IphoneCollector(collector.BaseCollector):

    def fetch(self):
        self.fetch_into()

    def init(self):
        self.fetch_info(INIT=True)

    def fetch_info(self, INIT=False):
        parser = etree.HTMLParser(encoding='utf-8')
        self.logger.info('start fetching from app111.com')

        text=urllib2.urlopen(FIRST_PAGE_URL).read(-1)
        tree=etree.HTML(text,parser=parser)
        nodes=tree.xpath(LIST_CATEGORY_XPATH)

        #get all categories' paths
        category_paths=[]
        for node in nodes:
            category_paths.append(node.attrib['href'][:-1])
        print category_paths

        #analysis each category, skip category_paths[0] this time
        for category_path in category_paths[1:]:

            text=urllib2.urlopen(category_path).read(-1)
            tree=etree.HTML(text,parser=parser)

            page_num_path=tree.xpath(PAGE_NUM_XPATH)
            page_num=page_num_path[0].text.strip()[2:]      #get the total page number in that category

            #set the page range: page_num for the first time, and less for increment
            if INIT:
                pages=range(1,int(page_num)+1)
            else:
                pages=range(1,INCREMENT+1)

            for page in pages:
                cur_path=category_path[:-1]+str(page)
                self.logger.info(cur_path)
                text=urllib2.urlopen(cur_path).read(-1)
                tree=etree.HTML(text,parser=parser)
                nodes=tree.xpath(LIST_XPATH)
                print 'OK'
                
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
                        self.logger.info("%s:%s - %s" %(time,title,url))
                        collector.object_found.send(self,time=time,title=title,url=url)
                    except:
                        self.logger.info(time)
            
        '''
        #pages=range(1,1000)
        pages=range(1,616)
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
         '''
