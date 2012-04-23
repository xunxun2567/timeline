import urllib2
from lxml import etree
from kernel import collector

#LIST_URL = 'http://searchjob.chinahr.com/Shanghai--searchresult.html?occIDList&occParentIDList=100&myLocIDList=31000&myLocPa#rentIDList=31000&isInterView=1&IsModel=false&from=search&prj=quick&page=2'

LIST_URL = 'http://campus.chinahr.com/Campus/Search/joblist.aspx?Type=Search&KeyWord=&JobLocation=&JobDateTime=&PageIndex=%d&PageSize=20'

#LIST_URL = 'http://searchjob.chinahr.com/GetSearchResult.awp?jtq=onlyrecord&urlKey=b2NjSURMaXN0JTI2b2NjUGFyZW50SURMaXN0JTNEMTAwJTI2bXlMb2NJRExpc3QlM0QzMTAwMCUyNm15TG9jUGFyZW50SURMaXN0JTNEMzEwMDAlMjZpc0ludGVyVmlldyUzRDElMjZJc01vZGVsJTNEZmFsc2UlMjZmcm9tJTNEc2VhcmNoJTI2cHJqJTNEcXVpY2slMjZzaiUzRDElMjZjdXJQYWdlJTNEMiUyNnBhZ2VTaXplJTNEMzAlMjZyZWNvcmRDb3VudCUzRDc0Njc0JTI2b3JkZXJGaWVsZCUzRFJlZnJlc2hEYXRlJTI2b3JkZXIlM0RERVND&ProjectID=3&IsModel=false&jtr=12982899&jtrr='

LIST_XPATH = '//*[@id="jobView"]/tr[position()>1]'
TITLE_PATH = 'td[2]/a'
DATE_PATH = 'td[6]/span'

class WWWChinaHRJobCollector(collector.Collector):
    def pull(self):
        print "WWWChinaHRJobCollector pulling from topic collector!!"

    def clone(self):
        print "Start cloning from www.chinahr.com..."
        parser = etree.HTMLParser(encoding='gbk')

        pages = range(1, 10)
        for page in pages:
            headers = { 'Referer': 'http://campus.chinahr.com/Campus/Search/joblist.aspx' }
            request = urllib2.Request(LIST_URL % page, None, headers)
            text = urllib2.urlopen(request).read(-1)
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(LIST_XPATH)
            for node in nodes:
                node1 = node.find(TITLE_PATH)
                title = node1.text
                url = node1.attrib['href']
                node2 = node.find(DATE_PATH)
                time = node2.text.strip()
                print "%s: %s - %s" % (time, title, url)
                collector.object_found.send(self, time=time, title=title, url=url)
