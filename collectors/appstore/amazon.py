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

PROXY_ENABLE=False
INCREMENT=3 #DEFINE THE PAGE TO BE VIEWED FOR INCREMENT
INIT_PAGES=100

def url_save_open(url):
    retry=3
    while retry:
        try:
            link=urllib2.urlopen(url)
            text=link.read(-1)
            return text
        except :
            retry=retry-1
            sleep(1)
    print "Page cannot be opened right now, jump to the next page"
    return None

class AmazonCNCollector(collector.BaseCollector):
    def fetch(self):
        print 'start fetch amazon.cn'
        self.fetch_info(INCREMENT)

    def init(self):
        print 'start fetch amazon.cn for the 1st time'
        self.fetch_info(INIT_PAGES)
    
    def fetch_info(self,PAGE_NUM):
        MAX_PAGE=PAGE_NUM
        parser=etree.HTMLParser(encoding='utf-8')

        #install proxy opener
        if PROXY_ENABLE:
            proxy_support=urllib2.ProxyHandler({'http':'hdqsmsg01/xukf:tiancai0-=)_+@proxy.spdb.com:8080'})
            opener=urllib2.build_opener(proxy_support,urllib2.HTTPHandler)
            urllib2.install_opener(opener)

        #get the 2nd-level categories' URLs, total number is around 700
        text=url_save_open(CATEGORY_URL)
        if text is not None:
            tree=etree.HTML(text,parser=parser)
            nodes=tree.xpath(CATEGORY_XPATH)
        else:
            print "FATAL: first page cannot be read"

        categories_url=[]
        for node in nodes:
            url_path=node.attrib['href']
            categories_url.append(url_path)

        #get the 3rd-level categories' URLs
        for category_url in categories_url[1:]:
            #get the 3rd-level categories' URLs
            text_1=url_save_open(category_url)
            if text is not None:
                print "URL_1 successfully opened"
                try:
                    tree_1=etree.HTML(text_1,parser=parser)
                    nodes_1=tree_1.xpath(CATEGORY_XPATH_2ND)
                except :
                    print "URL_1 Parser failed, next please..."
                    continue
            else:
                print "URL_1 opened failed, next please..."
                continue

            categories_url_3rd=[]
            for node_1 in nodes_1:
                node1=node_1.find('a')
                try:
                    url=node1.attrib['href']
                    categories_url_3rd.append(url)
                except :
                    categories_url_3rd=[]

            #parse the page info
            if categories_url_3rd==[]:
                print "Cannot get the URL list..."
                continue


            for page_url in categories_url_3rd:
                pages=range(1,MAX_PAGE+1)
                pos=page_url.find('&page=')
                for page in pages:
                    cur_URL=page_url[:pos]+'&page='+str(page)
                    text_2=url_save_open(cur_URL)
                    if text_2 is not None:
                        try:
                            tree_2=etree.HTML(text_2,parser=parser)
                            nodes_2=tree_2.xpath(CATEGORY_XPATH_3RD)
                        except :
                            print "URL_2 Parser failed, next please..."
                    else:
                        print "URL_2 opened failed, next please..."
                        continue

                    for node_2 in nodes_2:
                        node1=node_2.find(TITLE_XPATH)
                        try:
                            title=node1.text.strip()
                            url=node1.attrib['href']
                            if len(url)>500:
                                continue
                            url=url.encode('utf-8')
                            node2=node_2.find(TIME_XPATH)
                            time=node2.text.strip()[1:8]
                            time=time+'-01'
                        except:
                            continue
                        self.logger.info("%s:%s - %s" %(time,title,url))
                        collector.object_found.send(self,time=time,title=title,url=url,check=True)

            


            