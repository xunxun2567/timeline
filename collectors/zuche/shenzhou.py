#.-.coding=utf8

__author__ = 'konglingkai'

import urllib
import urllib2
import cookielib
import os
import time
from lxml import etree
from kernel import collector

cookie_filename = 'shenzhou.cookies'

FIRST_PAGE_URL = 'http://www.zuche.com'
FORM_UNIQUE_ID_XPATH = '//*/input[@id="_form_uniq_id"]'

SECOND_PAGE_URL = 'http://www.zuche.com/order/OrderSecondJsonControl.do_'
THIRD_PAGE_URL = 'http://www.zuche.com/jsp/order/personalOrderSecond.jsp?cid=81152&origin=shortRent'

ITEM_XPATH = '//*/table[@class="order_list_tab"]/tr[position()>1]'
CAR_NAME = 'td[2]/p'
CAR_PRICE = 'td[3]/font[1]'

class ShenZhouCollector(collector.Collector):

    def __init__(self):
        self.cj = cookielib.MozillaCookieJar(cookie_filename)
        if os.access(cookie_filename, os.F_OK):
            self.cj.load()
        self.opener = urllib2.build_opener(
            urllib2.HTTPRedirectHandler(),
            urllib2.HTTPHandler(debuglevel=0),
            urllib2.HTTPSHandler(debuglevel=0),
            urllib2.HTTPCookieProcessor(self.cj)
        )
#        self.opener.addheaders = [
#            ('User-agent', 'Mozilla/5.0'),
#            ('X-Requested-With', 'XMLHTTPRequest'),
#            ('Referer', 'http://www.zuche.com/'),
#            ('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8'),
#            ('Pragma', 'no-cache'),
#            ('Cache-Control', 'no-cache'),
#            ('Connection', 'keep-alive'),
#            ('Accept', 'application/json, text/javascript, */*')
#        ]

    def fetch(self):
        self.search(5, 4, 6, 449)

    def search(self, month, day, city_id, store_id):
        text = self.opener.open(FIRST_PAGE_URL).read()
        print 'step 1 succeed...'
        time.sleep(3)

        parser = etree.HTMLParser(encoding='utf8')
        tree = etree.HTML(text, parser)
        nodes = tree.xpath(FORM_UNIQUE_ID_XPATH)
        unique_id = nodes[0].attrib['value']

        params = {
                'leaseterm_year' : '0',
                'fromMinute' : '00',
                'fromDate' : '2012-%02d-%02d' % (month, day),
                'toMinute' : '00',
                'toDate' : '2012-%02d-%02d' % (month, day),
                'servicetype' : '6',
                'fromstoreId' : '%d' % store_id,
                'fromHour' : '10',
                'vehiclebrand' : '0',
                'tostoreId' : '%d' % store_id,
                'shortColor' : 'shortRent',
                'fromHourData' : '10',
                'serviceMode' : '1',
                'senttype' : '0',
                'toHour' : '20',
                'tocityid' : '%d' % city_id,
                'fromcityid' : '%d' % city_id,
                'fromTime' : '2012-%02d-%02d 10:00' % (month, day),
                'leaseterm_month' : '0',
                'rentDay' : '3',
                'picktype' : '0',
                'toTime' : '2012-%02d-%02d 20:00' % (month, day),
                'vehiclemode' : '0',
        }

        search_params = {
            'paramData': urllib.urlencode(params),
            'step': 'first',
            '_form_uniq_id': unique_id
        }

        data = urllib.urlencode(search_params)
        text = self.opener.open(SECOND_PAGE_URL, data).read()
        if text == '[]':
            print 'Step 2 succeed...'
        else:
            print 'Step 2 Failed!...'

        text = self.opener.open(THIRD_PAGE_URL).read()
        print text
        print 'Step 3 succeed...'

        tree = etree.HTML(text, parser)
        nodes = tree.xpath(ITEM_XPATH)
        for node in nodes:
            car_name = node.find(CAR_NAME).text
            car_price = node.find(CAR_PRICE).text
            print '%s: %s' % (car_name, car_price)

        print '%d items found.' % len(nodes)
        self.cj.save()