#.-.coding=utf8

__author__ = 'xukaifang'


import urllib2
from lxml import etree
from kernel import collector
import datetime

MENU_PAGE_URL='http://as.baidu.com/a?pre=web_am_header&f=web_alad_1/'
LIST_CATEGORY_XPATH1='/html/body/div/section/aside/section[2]/ul/li[position()>0]'
LIST_CATEGORY_XPATH2='/html/body/div/section/aside/section[3]/ul/li[position()>0]'
CATEGORY_XPATH='a'

LIST_XPATH='/html/body/section/section/section/ul/li[position()>0]'
LIST_PAGE_URL_MENU='http://as.baidu.com/a/software?cid=501&pre=web_am_index&f=web_alad_1'
LIST_PAGE1_URL='http://as.baidu.com/a/software?cid=501&s=1&f=web_alad_1'
LIST_PAGE2_URL='http://as.baidu.com/a/software?cid=501&s=1&f=web_alad_1&pn=2'
TITLE_PATH='a/div[2]/div/h4'
URL_PATH='a'
TIME_PATH='a/div[2]/div[2]/span[4]'

INCREMENT=3 #DEFINE THE PAGE TO BE VIEWED FOR INCREMENT
INIT_PAGES=50

class AndroidCollector(collector.BaseCollector):
    def fetch(self):
        self.fetch_info(INCREMENT)

    def init(self):
        self.fetch_info(INIT_PAGES)

    def fetch_info(self,PAGE_NUM):
        MAX_PAGE=PAGE_NUM
        parser = etree.HTMLParser(encoding='utf-8')
        self.logger.info('start fetching from as.baidu.com')

        text=urllib2.urlopen(MENU_PAGE_URL).read(-1)
        tree=etree.HTML(text,parser=parser)
        nodes=tree.xpath(LIST_CATEGORY_XPATH1)
        nodes.extend(tree.xpath(LIST_CATEGORY_XPATH2))

        #get all categories' paths
        category_paths=[]
        for node in nodes:
            url=node.find(CATEGORY_XPATH)
            url_path=url.attrib['href']
            url_pos=url_path.find('&')
            url_path=url_path[:url_pos]
            category_paths.append(url_path)
        self.logger.info(category_paths)
        
        #analysis each category, skip category_paths[0] this time
        for category_path in category_paths:
            pages=range(1,MAX_PAGE+1)   #each category only has 50 pages
            for page in pages:
                cur_path=category_path+'&s=1&pn='+str(page)
                print cur_path
                text=urllib2.urlopen(cur_path).read(-1)
                tree=etree.HTML(text,parser=parser)
                nodes=tree.xpath(LIST_XPATH)

                for node in nodes:
                    try:
                        node1=node.find(TITLE_PATH)
                        title=node1.text.strip()
                        node2=node.find(URL_PATH)
                        url=node2.attrib['href']
                        node3=node.find(TIME_PATH)
                        time=node3.text.strip()
                        time=time[-10:]     #time format
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
