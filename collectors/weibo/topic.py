import urllib2
import datetime
import json
import kernel.collector
from kernel import collector

LIST_URL = 'http://news.sina.com.cn/iframe/tblog/js/hottopic/jsondata_new.js'
#LIST_XPATH = '//*/ul[@id=S_Cont_0]'

class TopicCollector(collector.Collector):
    def fetch(self):
        #print "cloning from mimi collector!!"
        print "Start cloning topics from weibo.com..."
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        text = urllib2.urlopen(LIST_URL).read(-1)
        text = text[len(r'/* 1,729,12 2012-04-30 22:00:07 */\nvar jsondata='):len(text)]
        data = json.loads(text,encoding='gbk')
        topics = data["result"]
        for topic in topics:
            for subtopic in topic:
                title = subtopic["topic"]
                url = subtopic["url"]
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)
        #topics = text["result"]
        #print topics
        """
        parser = etree.HTMLParser(encoding='utf-8')
        tree = etree.HTML(text, parser=parser)
        nodes = tree.xpath(LIST_XPATH)
        print nodes
        for node in nodes:
            title = node.text
            url = node.attrib['href']
            print "%s: %s - %s" % (time, title, url)
            #collector.object_found.send(self, time=time, title=title, url=url)
        """
