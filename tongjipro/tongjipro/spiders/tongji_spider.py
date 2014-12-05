#-*- coding: utf-8 -*-
import sys
from urlparse import urljoin
from scrapy.http import Request

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector,Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tongjipro.items import tongjiproItem

import datetime
add = 0
sys.stdout = open('output.txt','w');

#class fjsenSpider(BaseSpider):
class fjsenSpider(CrawlSpider):
    name="tongji"
    allowed_domains=[]
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html']
    #start_urls=['http://www.fjsen.com/j/node_94962_'+str(x)+'.htm' for x in range(2,11)]+['http://www.fjsen.com/j/node_94962.htm']
    rules = (
            Rule(SgmlLinkExtractor(allow=(r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/.*\.html')),callback='parse_item',follow='true'),
            #Rule(SgmlLinkExtractor(allow=(r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/.*/.*/.*/.*\.html')),callback='parse_item',follow='true'),
            #Rule(SgmlLinkExtractor(allow=(r'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013')),callback='parse_item',follow='true'),
    )
			
#    def parse_item(self,response):
#        print '===parse_qu===\n'
#        item=tongjiproItem()
#        hxs=HtmlXPathSelector(response)
        #sites=hxs.select('//tr[@class=\'provincetr\']/td')
#        global add
#        print 'add = ',add
#        add+=1
#        item['id']=add
#        titles = hxs.select('//tr[@class=\'provincetr\']/td/a/text()').extract()
#        item['title'] = titles and titles[0] or ''
#        #item['title'] = titles[0]
#        links=hxs.select('//tr[@class=\'provincetr\']/td/a/@href').extract()
#        item['link'] = links and links[0] or ''
#        addtimes=hxs.select('//span/text()').extract()
#        item['addtime'] = addtimes and addtimes[0] or ''
#        print item
#        return item

    def parse_item(self,response):
        item = tongjiproItem()
        sel = Selector(response)

        global add
        print 'add= ',add
        add+=1

        item['id']=add

        #province = sel.xpath('//tr[@class=\'provincetr\']/td/a/text()').extract()
        #省(直辖市) >> 市(直辖区,) >> 区 >> 镇(街道) >> 村
        county = sel.xpath('//tr[@class=\'provincetr\']/td/a/text() | //tr[@class=\'citytr\']/td[position()=2]/a/text() | //tr[@class=\'contytr\']/td[position()=2]/a/text() | //tr[@class=\'towntr\']/td[position()=2]/a/text() | //tr[@class=\'villagetr\']/td[position()=3]/text()').extract()
        #town = sel.xpath('//tr[@class=\'towntr\']/td/a/text()').extract()
        #village = sel.xpath('//tr[@class=\'villagetr\']/td/a/text()').extract()

        #print 'titles = ',province
        #item['title'] = sel.xpath('//tr[@class=\'provincetr\']/td/a/text()').extract()[0]
        item['title']=county and county[0] or ''
        #print 'oooooooooo',county

        #province_links = sel.xpath('//tr[@class=\'provincetr\']/td/a/@href').extract()
        item['link'] = response.url

        #addtimes = sel.xpath('//span/text()').extract()
#        item['addtime'] = addtimes and addtimes[0] or ''
        #item['addtime']=datetime.datetime.now()
        print item
        return item



#    def parse2(self,response):
#        hxs=HtmlXPathSelector(response)
#        sites=hxs.select('//tr[@class=\'provincetr\']/td')
#        items=[]
#        global add

#        for site in sites:
#            add+=1
#            item=tongjiproItem()
#            item['id']=add
#            item['title']=site.select('a/text()').extract()
#            item['link'] = site.select('a/@href').extract()
#            item['addtime']=site.select('span/text()').extract()
#            items.append(item)
#        print '=====parse=====\n'
#        return items  





