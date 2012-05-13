#.-.coding=utf8

__author__ = 'konglingkai'

import urllib
import urllib2
import cookielib
import os
import xlwt
import json
import datetime
from lxml import etree
from kernel import collector

cookie_filename = 'shenzhou.cookies'

FIRST_PAGE_URL = 'http://www.zuche.com'
FORM_UNIQUE_ID_XPATH = '//*/input[@id="_form_uniq_id"]'

SECOND_PAGE_URL = 'http://www.zuche.com/order/OrderSecondJsonControl.do_'
THIRD_PAGE_URL = 'http://www.zuche.com/jsp/order/personalOrderSecond.jsp?cid=81152&origin=shortRent'

ITEM_XPATH = '//*/table[@class="order_list_tab"]/tr[position()>1]'
CAR_NAME = 'td[2]/p'
CAR_PRICE = 'td[5]/div[1]/font[1]'
CAR_ALL_PRICES = 'td[5]/div[1]/font[2]/div[1]/ul[2]/li'



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
        today = datetime.datetime.now()
        month = today.month
        day = today.day
        book = xlwt.Workbook(encoding='utf-8')
        text = self.opener.open('http://www.zuche.com/city/getCityJson.do_', 'cityname=').read()
        cities = json.loads(text)
        for city in cities:
            city_id = city['code']
            city_name = city['name']
            if city_id == '-1': break
            print '%s: %s' % (city_id, city_name)
            sheet = book.add_sheet(city_name)
            text = self.opener.open('http://www.zuche.com/department/getDepartmentJson.do_', 'cityId=%s' % city_id).read()
            stores = json.loads(text)
            row = 0
            for store in stores:
                store_id = store['code']
                store_name = store['name']
                store_addr = store['address']
                service_type = store['serviceType']
                print "    [%s]%s: %s - %s" % (service_type, store_id, store_name, store_addr)
                cars = self.search(month, day, city_id, store_id, service_type)
                for car_name, car_price, car_prices in cars:
                    today_string = today.strftime('%Y-%m-%d')
                    sheet.write(row, 0, today_string)
                    sheet.write(row, 1, city_name)
                    sheet.write(row, 2, store_name)
                    sheet.write(row, 3, car_name)
                    sheet.write(row, 4, car_price)
                    row += 1
                    print '2012-%02d-%02d %s %s %s %s' % (month, day, city_name, store_name, car_name, car_price)
                    collector.object_found.send(
                        self,
                        time=today_string,
                        url='http://www.shenzhou.com',
                        title='%s %s %s %s' % (city_name, store_name, car_name, car_price),
                        check=False,
                        city=city_name,
                        mendian=store_name,
                        chexing=car_name,
                        check_date=today_string,
                        book_date=today_string,
                        price=car_price
                    )

                    book_date = datetime.datetime.now()
                    for price in car_prices:
                        book_date = book_date + datetime.timedelta(days=1)
                        collector.object_found.send(
                            self,
                            time=today_string,
                            url='http://www.shenzhou.com',
                            title='%s %s %s %s' % (city_name, store_name, car_name, car_price),
                            check=False,
                            city=city_name,
                            mendian=store_name,
                            chexing=car_name,
                            check_date=today_string,
                            book_date=book_date.strftime('%Y-%m-%d'),
                            price=price
                        )
        book.save('shenzhou_%02d_%02d.xls' % (month, day))

    def search(self, month, day, city_id, store_id, service_type):
        text = self.opener.open(FIRST_PAGE_URL).read()
        print 'step 1 succeed...'

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
                'servicetype' : '%s' % service_type,
                'fromstoreId' : '%s' % store_id,
                'fromHour' : '10',
                'vehiclebrand' : '0',
                'tostoreId' : '%s' % store_id,
                'shortColor' : 'shortRent',
                'fromHourData' : '10',
                'serviceMode' : '1',
                'senttype' : '0',
                'toHour' : '20',
                'tocityid' : '%s' % city_id,
                'fromcityid' : '%s' % city_id,
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
        print 'Step 3 succeed...'

        result = []
        tree = etree.HTML(text, parser)
        nodes = tree.xpath(ITEM_XPATH)

        for node in nodes:
            car_name = node.find(CAR_NAME).text
            car_price = node.find(CAR_PRICE).text
            car_all_prices = node.findall(CAR_ALL_PRICES)
            car_prices = []
            for car_price_node in car_all_prices:
                p = car_price_node.find('span')
                if p != None:
                    car_prices.append(p.text)
                    if len(car_prices) == 14: break
            result.append((car_name, car_price, car_prices))

        print '%d items found.' % len(nodes)
        self.cj.save()

        return result
