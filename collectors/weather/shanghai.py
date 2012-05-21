# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

LIST_URL = 'http://www.weather.com.cn/weather/101020100.shtml'

LIST_XPATH = '//*[@id="7d"]/div/table[2]'
DATE_PATH = 'tr/td/a'
DAYWEA_PATH = 'tr/td[4]/a'
NIGHTWEA_PATH='tr[2]/td[3]/a'
HIGHTEMP_PATH='tr/td[5]/a/span/strong'
LOWTEMP_PATH='tr[2]/td[4]/a/span/strong'

def print_dict(dict):
    for key in dict:
        print u"%s:%s" % (key, dict[key])

class ShanghaiCollecotr(collector.BaseCollector):
    def fetch(self):
        time = datetime.datetime.now().date().strftime('%Y-%m-%d')
        self.logger.info("Start cloning from www.weather.com.cn...")
        parser = etree.HTMLParser(encoding='utf-8')
        text = urllib2.urlopen(LIST_URL).read(-1)
        tree = etree.HTML(text, parser=parser)

        weaDict = {}
        nodes = tree.xpath(LIST_XPATH)
        for node in nodes:
            node1 = node.find(DATE_PATH)
            dateDay = node1.text
            dateDay = dateDay[0:dateDay.index(u'日')]
            curDay = datetime.datetime.now().date().day
            if int(dateDay) != int(curDay):
                self.logger.error(u"错误！天气预报日期%s日不是当前日期%s日" % (dateDay, curDay))
                return
            node2 = node.find(DAYWEA_PATH)
            #print node2.text
            node3 = node.find(HIGHTEMP_PATH)
            #print node3.text
            curHour = datetime.datetime.now().time().hour
            if int(curHour) >= 18 or int(curHour) <= 8 :
                weaDict[u"夜间"] = node2.text
                weaDict[u"低温"] = node3.text
                self.logger.info(u"现在时间%s:00,已超过18:00，只能取夜间天气" % curHour)
                self.logger.info(time)
                print_dict(weaDict)
                return
            weaDict[u"白天"] = node2.text
            weaDict[u"高温"] = node3.text
            node4 = node.find(NIGHTWEA_PATH)
            weaDict[u"夜间"] = node4.text
            node5 = node.find(LOWTEMP_PATH)
            weaDict[u"低温"] = node5.text

            self.logger.info(time)
            print_dict(weaDict)
            #collector.object_found.send(self, time=time, title=title, url=url)
"""
        for node in nodes:
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                #datetime.strptime - can you please work with unicode???
                time = node2.text.replace(u'年', '-').replace(u'月', '-').replace(u'日', '-')
                time = datetime.datetime.strptime(time, '%Y-%m-%d-')
                print "%s: %s - %s" % (time, title, url)

      """