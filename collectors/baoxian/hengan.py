#.-.coding=utf8

__author__ = 'konglingkai'

import urllib
import urllib2
import cookielib
import os
import json
from lxml import etree
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
        text = self.opener.open(FIRST_PAGE_URL).read()
        print "getting validate code..."
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
        print 'Done.'
        text = self.opener.open(CONFIG_PAGE_URL).read()
        #print text
        insuranceDocument = '{\
            "policyHolder":{\
                "cid":null,\
                "name":"老张",\
                "sex":"F",\
                "age":30,\
                "birthday":"1982-05-09"\
            },\
            "insurant":{\
                "name":"老张",\
                "sex":"F",\
                "pregnant":false,\
                "age":30,\
                "birthday":"1982-05-09",\
                "isPolicyHolder":true,\
                "jobCode":"AA01",\
                "jobName":"职员、公务员",\
                "lifeRiskLevel ":"标准费率",\
                "accidentRiskLevel":"1",\
                "hospitalRiskLevel":"1"\
            },\
            "insuranceArray":[{\
                "insureId":"38",\
                "code":"CAD",\
                "name":"CAD-珍爱相随A款",\
                "kind":"main",\
                "premium":null,\
                "risk":"20000",\
                "riskView":"20000",\
                "risk_unit":"元",\
                "policyPeriod":"@99",\
                "policyPeriod_text":"至99周岁",\
                "policyPeriodYear":69,\
                "payPeriod":"5",\
                "payPeriod_text":"5年缴",\
                "payPeriodType":"year",\
                "payPeriodType_text":"年缴",\
                "drawAge":null,\
                "drawAge_text":null,\
                "children":[]\
            }]\
        }'
        data = { 'insuranceDocument': insuranceDocument }
        text = self.opener.open(ITEM_PAGE_URL, urllib.urlencode(data)).read()

        text = self.opener.open(PROFIT_PAGE_URL, urllib.urlencode(data)).read()

        data = json.loads(text)
        headers = data['interestDataHeaderList']
        for header in headers:
            print header['value']

        data = json.loads(text)['interestDataList']
        for row in data:
            print '%s: %s' % (row['ia'], row['sumPby'])





