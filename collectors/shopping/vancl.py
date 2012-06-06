# .-. coding=utf-8
import urllib2
import datetime
from lxml import etree
from kernel import collector

BASE_URL = 'http://s.vancl.com/search?p=%d&s=1'
#MEN_CLOTHING_URL = 'http://s.vancl.com/1667.html?p=%d'
#WOMEN_CLOTHING_URL = 'http://rihan.vancl.com/search/?navtype=02&cateid=4225&page=%d'
#KID_CLOTHING_URL = 'http://children.vancl.com/search/?navtype=08&page=%d'
#MEN_SHOES_URL = 'http://s.vancl.com/1866.html?p=%d'
#WOMEN_SHOES_URL = 'http://nvxie.vancl.com/search/?navtype=09&cateid=2907%2c3730%2c1955&page=%d'
#ACCESSORIES_URL = 'http://accessories.vancl.com/search/?orderby=1&page=%d'
#BAG_URL = 'http://bag.vancl.com/search/?page=%d'

XPATH = '//*/div[@id="vanclproducts"]/ul/li'

class VanclCollector(collector.BaseCollector):
    def fetch(self):
        self.logger.info('Vancl started.')
        self.getData(BASE_URL,100)
        #self.getData(MEN_CLOTHING_URL,10, u'男装')
        #self.getData(WOMEN_CLOTHING_URL,9,u'女装')
        #self.getData(KID_CLOTHING_URL,45,u'童装')
        #self.getData(MEN_SHOES_URL,10,u'男鞋')
        #self.getData(WOMEN_SHOES_URL,9,u'女鞋')
        #self.getData(ACCESSORIES_URL,66,u'配件')
        #self.getData(BAG_URL,31,u'箱包')

    def getData(self, url, pages):
        parser = etree .HTMLParser(encoding='utf-8')
        for page in range(28, pages):
            self.logger.info('Page: %d:' % page)
            #text = urllib2.urlopen(BASE_URL % page).read()
            text = urllib2.urlopen(url % page).read()
            tree = etree.HTML(text, parser=parser)

            time = datetime.datetime.now().strftime('%Y-%m-%d')
            nodes = tree.xpath(XPATH)
            for node in nodes:
                sub_node = node.find('div[1]/a')
                title = sub_node.attrib['title']
                ourl = sub_node.attrib['href']
                image_url = sub_node.find('img').attrib['original']
                sub_node = node.find('div[2]/span[2]')
                price = sub_node.text.strip()
                sub_node = sub_node.find('strong')
                if sub_node is not None:
                    price += sub_node.text
                price = price[len(u"售价"):len(price)]

                if u'包' in title or u'箱' in title:
                    leibie = u'箱包'
                elif u'男童' in title or u'女童' in title or u'儿童' in title:
                    leibie = u'童装'
                elif u'鞋' in title or u'拖' in title:
                    if u'女' in title or u'girl' in title:
                        leibie = u'女鞋'
                    else:
                        leibie = u'男鞋'
                elif u'帽' in title or u'腰封' in title or u'腰带' in title or u'太阳镜'in title or u'项链' in title or u'耳' in title\
                or u'发绳' in title:
                    leibie = u'配饰'
                elif u'女' in title or u'裙'in title or u'丽人'in title or u'荷叶'in title or u'Candy'in title:
                    leibie = u'女装'
                else:
                    leibie = u'男装'
                self.logger.info('%s(%s) - %s @ %s - %s' % (title, price, ourl, image_url, leibie))
                collector.object_found.send(
                    self,
                    time = time, title = title, url = ourl,
                    image_url = image_url,
                    price = price,
                    leibie = leibie
                )