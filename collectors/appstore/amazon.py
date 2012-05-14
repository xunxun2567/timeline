#.-.coding=utf8

__author__ = 'xukaifang'

import urllib2
from lxml import etree
from kernel import collector
from time import sleep
'''
amazon.cn has a 3-level book category.
URL of the second level category can be found through CATEGORY_URL.
URL of the third level category can be found through CATEGORY_URL_2ND
'''
###Category 1st
CATEGORY_URL='http://www.amazon.cn/gp/feature.html/ref=sv_b_1?ie=UTF8&docId=42108'
#CATEGORY_XPATH='/html/body/table/tbody/tr/td/table/tbody/tr/td/div/ul'
CATEGORY_XPATH='/html/body/table/tr/td/table/tr/td/div/ul/li/a'      #why we must delete tbody?

###Category 2nd
CATEGORY_URL_2ND='http://www.amazon.cn/s?ie=UTF8&rh=n%3A658390051%2Cn%3A%21658391051%2Cn%3A658394051%2Cn%3A658508051&page=1'
CATEGORY_URL_2ND_1='http://www.amazon.cn/s/ref=sr_nr_n_2?rh=n%3A658390051%2Cn%3A!658391051%2Cn%3A658395051&bbn=658391051&ie=UTF8&qid=1336913177&rnid=658391051'
CATEGORY_XPATH_2ND='/html/body/div[2]/div[3]/div[2]/div/div/ul[1]/li'
#CATEGORY_XPATH_2ND='/html/body/div[3]/div[3]/div[2]/div/div/ul/li[4]'

###CATEGORY 3rd
CATEGORY_URL_3RD='http://www.amazon.cn/s?ie=UTF8&rh=n%3A659359051&page=1'
CATEGORY_XPATH_3RD='//*[@id="atfResults"]/div/div | //*[@id="btfResults"]/div/div'
TITLE_XPATH='div/div/a'
TIME_XPATH='div/div/span[3]'

PROXY_ENABLE=True
class AmazonCNCollector(collector.Collector):
    def fetch(self):
        parser=etree.HTMLParser(encoding='utf-8')
        print 'start fetch amazon.cn'

        #install proxy opener
        if PROXY_ENABLE:
            proxy_support=urllib2.ProxyHandler({'http':'hdqsmsg01/xukf:tiancai0-=)_+@proxy.spdb.com:8080'})
            opener=urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)
            
        '''
        #get the 2nd-level categories' URLs, total number is around 700
        text=urllib2.urlopen(CATEGORY_URL).read(-1)
        tree=etree.HTML(text,parser=parser)
        nodes=tree.xpath(CATEGORY_XPATH)

        categories_url=[]
        for node in nodes:
            url_path=node.attrib['href']
            categories_url.append(url_path)
        '''

        '''
        #get the 3rd-level categories' URLs
        for category_url in categories_url[1]:
            #get the 3rd-level categories' URLs
            try:
                text=urllib2.urlopen(category_url).read(-1)
            except:
                sleep(1);
                text=None
                text=urllib2.urlopen(category_url).read(-1)
            
            tree=etree.HTML(text,parser=parser)
            nodes=tree.xpath(CATEGORY_XPATH_2ND)
            categories_url_3rd=[]

            for node in nodes:
                node1=node.find('a')
                try:
                    url=node1.attrib['href']
                    categories_url_3rd.append(url)
                except :
                    categories_url_3rd=[]

        print nodes
        print categories_url_3rd
        print len(categories_url_3rd)
        '''

        #parse the page info
        '''
        MAX_PAGE=100
        for page_url in categories_url_3rd:
            pages=range(1,MAX_PAGE+1)
            pos=page_url.find('&page=')
            for page in pages:
                cur_URL=page_url[:pos]+'&page='+str(page)
                try:
                    text=urllib2.urlopen(cur_URL).read(-1)
                except :
                    sleep(2)
                    text=None
                    text=urllib2.urlopen(cur_URL).read(-1)
                tree=etree.HTML(text,parser=parser)
                nodes=tree.xpath(CATEGORY_XPATH_3RD)

                for node in nodes:
                    pass
        '''
        text=urllib2.urlopen(CATEGORY_URL_3RD).read(-1)
        tree=etree.HTML(text,parser=parser)
        nodes=tree.xpath(CATEGORY_XPATH_3RD)

        for node in nodes:
            node1=node.find(TITLE_XPATH)
            title=node1.text.strip()
            url=node1.attrib['href']
            url=url.encode('utf-8')
            node2=node.find(TIME_XPATH)
            time=node2.text.strip()[1:8]
            time=time+'-01'

            print "%s:%s - %s" %(time,title,url)
            collector.object_found.send(self,time=time,title=title,url=url,check=True)
            
            

            