# coding=utf-8
__author__ = 'konglingkai'

from kernel import collector
import urllib2, cookielib, os
from PIL import Image
from lxml import etree

PAGE_URL = 'http://www.shjtaq.com/zwfg/dzjc_new.asp'
POST_DATA1 = 'cardqz=%BB%A6&carnumber='
POST_DATA2 = '&type1=02%2F%D0%A1%D0%CD%C6%FB%B3%B5%BA%C5%C5%C6&fdjh='
POST_DATA3 = '&verify='
POST_DATA4 = '&act=search&submit=+%CC%E1+%BD%BB+'
VALIDATE_CODE_URL = 'http://www.shjtaq.com/zwfg/validatecode.asp'
cookie_filename = '.data/weizhang/weizhang.cookies'
XPATH = '//*/table[@class="chinses1"]'

thumb_dna = [
# 0
[
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
],
# 1
[
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
],
# 2
[
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
    [0, 1, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 1, 1, 1, 1, 0],
],
# 3
[
    [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
],
# 4
[
    [1, 1, 1, 1, 1, 0, 0, 1, 1, 1],
    [1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
    [1, 1, 0, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 1, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 0, 1, 1, 0],
],
# 5
[
    [0, 0, 0, 0, 0, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 0, 0, 0, 1],
],
# 6
[
    [1, 1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 1, 1, 1, 1, 0, 0, 0, 0, 1],
],
# 7
[
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 1],
    [0, 1, 1, 1, 0, 0, 1, 1, 1, 1],
    [0, 1, 0, 0, 1, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
],
# 8
[
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
],
# 9
[
    [1, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 1, 0, 1, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1, 1],
]]

query_data = [
    ('BY8842', '252665'),
    ('BY8926', '253186'),
    ('BY8967', '83240012'),
#    ('DY6710', 'B8541508'),
    ('DY6883', '9C300153'),
    ('DY7102', '02090081'),
    ('L29899', 'B6140358'),
]

class WeizhangCollector(collector.BaseCollector):
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

    def fetch(self):
        self.logger.info(u'查询上海违章...')
        self.logger.info('Opening first page...')
        self.opener.open(PAGE_URL).read()
        self.logger.info('Done.')

        for number, engine in query_data:
            self.logger.info('Getting verify code...')
            text = self.opener.open(VALIDATE_CODE_URL).read()
            filename = '.data/weizhang/code.jpg'
            f = open(filename, 'w+')
            f.write(text)
            f.close()
            code = self.decode(filename)
            self.logger.info(code)

            self.logger.info('posting data...')
            text = self.opener.open(PAGE_URL, POST_DATA1 + number + POST_DATA2 + engine + POST_DATA3 + code + POST_DATA4).read()
            parser = etree.HTMLParser(encoding='gb2312')
            tree = etree.HTML(text, parser=parser)
            nodes = tree.xpath(XPATH)
            print '车牌：%s' % number
            print '上海电子监控:',
            print len(nodes[1].findall('tr')) > 4
            print '违章停车:',
            print len(nodes[2].findall('tr')) > 4
            print '外地电子监控:',
            print len(nodes[3].findall('tr')) > 4
            print


    def get_number(self, pixels):
        for x in range(6):
            dna = []
            for y in range(10):
                r,g,b = pixels[x, y]
                if r == 238 and g == 238 and b == 238:
                    dna.append(1)
                else:
                    dna.append(0)
            number = -1
            for src in thumb_dna:
                match = True
                for i in range(10):
                    if src[x][i] != dna[i]:
                        match = False
                        break
                if match:
                    number = thumb_dna.index(src)
                    break

            if number == -1:
                for x in range(6):
                    for y in range(10):
                        r,g,b = pixels[x, y]
                        if r == 238 and g == 238 and b == 238:
                            print 1,
                        else:
                            print 0,
                    print
            return number

    def decode(self, filename):
        image = Image.open(filename)
        c = (0, 0, 6, 10)
        pixels = image.crop(c).load()
        n1 = self.get_number(pixels)

        c = (10, 0, 16, 10)
        pixels = image.crop(c).load()
        n2 = self.get_number(pixels)

        c = (20, 0, 26, 10)
        pixels = image.crop(c).load()
        n3 = self.get_number(pixels)

        c = (30, 0, 36, 10)
        pixels = image.crop(c).load()
        n4 = self.get_number(pixels)

        return '%d%d%d%d' % (n1, n2, n3, n4)



