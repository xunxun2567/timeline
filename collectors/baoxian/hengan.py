#.-.coding=utf8

__author__ = 'konglingkai'

import urllib
import urllib2
import cookielib
import os
import json
from lxml import etree
import xlwt
from kernel import collector

cookie_filename = 'hengan.cookies'

FIRST_PAGE_URL = 'http://fat.hengansl.com:9080/hasl/agent/login.do?authenticationEntry=true'
VALIDATE_CODE_URL = 'http://fat.hengansl.com:9080/hasl/captcha.jpg'
LOGIN_URL = 'http://fat.hengansl.com:9080/hasl/agent/j_acegi_security_check.do'
CONFIG_PAGE_URL = 'http://fat.hengansl.com:9080/hasl/agent/ip/ProposalDesign/getIpConfigFile.do?_dc=1336539069720'
ITEM_PAGE_URL = 'http://fat.hengansl.com:9080/hasl/agent/ip/checkRule.do'
PROFIT_PAGE_URL = 'http://fat.hengansl.com:9080/hasl/agent/ip/ProposalDesign/getProfitGrid.do'

class HenganCollector(collector.BaseCollector):

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
        collector.BaseCollector.__init__(self)
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

    def get_data(self, product, sex, age, period, pay_period):
        insuranceDocument = '{"insurant":{\
            "sex":"%s",\
            "hospitalRiskLevel":"1",\
            "age":%d,\
            "birthday":"%d-06-04",\
            "name":"老王",\
            "pregnant":false,\
            "accidentRiskLevel":"1",\
            "jobCode":"AA01",\
            "isPolicyHolder":true,\
            "lifeRiskLevel ":"标准费率",\
            "jobName":"职员、公务员"},\
        "policyHolder":{\
            "sex":"%s",\
            "age":%d,\
            "birthday":"%d-06-04",\
            "name":"老王",\
            "cid":null},\
        "sumPremium":false,\
        "success":true,\
        "insuranceArray":[{\
            "payPeriodType":"year",\
            "drawType_text":null,\
            "riskView":100000,\
            "children":[],\
            "leaf":true,\
            "kind":"main",\
            "drawAge":null,\
            "risk":100000,\
            "payState":null,\
            "policyPeriodYear":50,\
            "insureId":"%s",\
            "policyPeriod":"%s",\
            "payPeriod":"%s",\
            "drawType":null,\
            "drawAge_text":null}],\
        "recordSelectArray":[]}'

        doc = insuranceDocument % (sex, age, 2012 - age, sex, age, 2012 - age, product, period, pay_period)

        data = { 'insuranceDocument': doc }
        text = self.opener.open(ITEM_PAGE_URL, urllib.urlencode(data)).read()
        text = self.opener.open(PROFIT_PAGE_URL, urllib.urlencode(data)).read()

        data = json.loads(text)

        return data;

    def fetch(self):
        text = self.opener.open(FIRST_PAGE_URL).read()
        self.logger.info("getting validate code...")
        text = self.opener.open(VALIDATE_CODE_URL).read()
        f = open('./code.jpg', 'w+')
        f.write(text)
        f.close()
        os.system('open ./code.jpg')
        code = raw_input('code is? ')
        data = {
            'j_username': '62001281002',
            'j_password': '11111111',
            'j_captcha_response': code
        }
        text = self.opener.open(LOGIN_URL, urllib.urlencode(data)).read()
        self.logger.info('Done.')
        text = self.opener.open(CONFIG_PAGE_URL).read()

        tree = etree.XML(text)
        nodes = tree.xpath('/insurList/insur')
        config = {}
        book = xlwt.Workbook(encoding='utf-8')
        sheet = book.add_sheet('产品列表')
        row = 0
        for node in nodes:
            id = node.attrib['id']
            config[id] = {}
            sub_1 = node.findall('attribute[@id="policyPeriod"]/item')
            config[id]['period'] = [sub_node.attrib['id'] for sub_node in sub_1]
            sub_2 = node.findall('attribute[@id="payPeriod"]/item')
            config[id]['payPeriod'] = [sub_node.attrib['id'] for sub_node in sub_2]
            sub_3 = node.find('property[@id="name"]')
            config[id]['name'] = sub_3.text
            sub_4 = node.find('property[@id="code"]')
            config[id]['code'] = sub_4.text
            sheet.write(row, 0, id)
            sheet.write(row, 1, config[id]['code'])
            sheet.write(row, 2, config[id]['name'])
            sheet.write(row, 3, str(config[id]['period']))
            sheet.write(row, 4, str(config[id]['payPeriod']))
            row += 1
        book.save('.data/hengan/products.xls')

        product = 49
        sex = 'M'
        age = 30
        period = '@80'
        pay_period = 5

        data = self.get_data(product, sex, age, period, pay_period);

        pby = data['interestDataList'][0]['pby']

        print product, sex, age, period, pay_period, pby

        return


        for product in config:
            product_dict = config[product]
            for sex in ('M', 'F'):
                for period in product_dict['period']:
                    for pay_period in product_dict['payPeriod']:
                        print product, sex, period, pay_period
                        book = xlwt.Workbook(encoding='utf-8')
                        for age in range(1, 80):
                            try:
                                print age
                                sheet = book.add_sheet('%d' % age)
                                data = self.get_data(product, sex, age, period, pay_period);

                                header_dict = {}
                                headers = data['interestDataHeaderList']
                                col = 0
                                for header in headers:
                                    header_dict[header['id']] = (col, header['value'])
                                    sheet.write(0, col, header['value'])
                                    col += 1

                                row = 1
                                for data_row in data['interestDataList']:
                                    for key in data_row:
                                        col,_ = header_dict[key]
                                        sheet.write(row, col, data_row[key])
                                    row += 1
                            except:
                                print 'fail..'

                        book.save('.data/hengan/%s_%s_%s_%s.xls' % (product, sex, period, pay_period));

#        headers = data['interestDataHeaderList']
#        for header in headers:
#            self.logger.info(header['value'])
#
#        data = json.loads(text)['interestDataList']
#        for row in data:
#            self.logger.info('%s: %s' % (row['ia'], row['sumPby']))





