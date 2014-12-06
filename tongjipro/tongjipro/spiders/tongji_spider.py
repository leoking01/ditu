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
add=0##province 的起点=0 总数31  净数=31
add_ci = 31##city  的起点=31  累计总数376=31+8+337  总数337+8  净数=337  8市直辖市数的二倍,因为还有县
add_cou =376 #county 的起点 376,净数=  1038
add_t = 1414 ##town 的起点 1414  
add_v = 13002 ##village 的起点 13002


sys.stdout = open('output.txt','w');



#################### parse province ########################
#class fjsenSpider(BaseSpider):
class provinceSpider(CrawlSpider):
    name="province"
    allowed_domains=['stats.gov.cn']
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013','parse']  ##  province起点
    #url=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013']
    #start_urls=['http://www.fjsen.com/j/node_94962_'+str(x)+'.htm' for x in range(2,11)]+['http://www.fjsen.com/j/node_94962.htm']
    rules = [
            #Rule(SgmlLinkExtractor(allow=['/.']),),
            #Rule(SgmlLinkExtractor(allow=['/.'+str(x)+'.html'for x in range(11,65) ] ),'parse_city'  ),
            #Rule(SgmlLinkExtractor(allow=['/.*'+'.*'+'.html'])),
            #Rule(SgmlLinkExtractor(allow=['/.*.html']),callback='parse_item',follow='false')
            #Rule(SgmlLinkExtractor(allow=['/.html']),callback='parse_item',follow='false')
    ]

    def parse(self,response):
        global add
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'provincetr\']/td')
        items=[]
        for site in sites:
            item=tongjiproItem()
            add+=1
            item['id']=add
            item['code']=site.select('a/@href').extract()
            item['title']=site.select('a/text()').extract()
            item['link']=site.select('a/@href').extract()
            #item['link']=response.url
            #item['addtime']=site.select('span/text()').extract()
            item['addtime']=site.select('a/@href').extract()
            items.append(item)
        #collect `item_urls`
        #for item_url in item_urls:
        #    yield Request(url=item_url, callback=self.parse_item)
        return items


##################### parse city  ######################
class citySpider(CrawlSpider):
    name="city"
    allowed_domains=['stats.gov.cn']
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'.html'for x in range(11,66) ] ##city 起点

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'citytr\']')
        items=[]
        global add_ci
        for site in sites:
            add_ci+=1
            item=tongjiproItem()
            item['id']=add_ci
            item['code']=site.select('td[position()=1]/a/text()').extract()
            item['title']=site.select('td[position()=2]/a/text()').extract()
            item['link'] = site.select('td[position()=1]/a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items  

##################### parse county  ######################
class countySpider(CrawlSpider):
    name="county"
    allowed_domains=['stats.gov.cn']
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(x)+str(y)+'.html'for x in range(11,66) for y in range(01,40) ] ##city 起点
    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'countytr\']')
        items=[]
        global add_cou
        for site in sites:
            add_cou+=1
            item=tongjiproItem()
            item['id']=add_cou
            item['code']=site.select('td[position()=1]/a/text()').extract()
            item['title']=site.select('td[position()=2]/a/text()').extract()
            item['link'] = site.select('td[position()=1]/a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items  

##################### parse  town  ######################
class townSpider(CrawlSpider):
    name="town"
    allowed_domains=['stats.gov.cn']
    #town 起点
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y)+'/'+str(x)+str(y)+str(z)+'.html'for x in range(11,66) for y in range(01,40)for z in range(0,40) ] 

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'towntr\']')
        items=[]
        global add_t
        for site in sites:
            add_t+=1
            item=tongjiproItem()
            item['id']=add_t
            item['code']=site.select('td[position()=1]/a/text()').extract()
            item['title']=site.select('td[position()=2]/a/text()').extract()
            item['link'] = site.select('td[position()=1]/a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items  

##################### parse  villege  ######################
class villegeSpider(CrawlSpider):
    name="villege"
    allowed_domains=['stats.gov.cn']
    #town 起点
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'++str(y)+'/'+str(z)+'/'+(str(x)+str(y)+str(z))+str(u)+'.html'for x in range(11,66) for y in range(01,40)for z in range(0,40) for u in range(01,999) ] 

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'villagetr\']')
        items=[]
        global add_v
        for site in sites:
            add_v+=1
            item=tongjiproItem()
            item['id']=add_v
            item['code']=site.select('td[position()=1]/a/text()').extract()
            item['title']=site.select('td[position()=3]/a/text()').extract()
            item['link'] = site.select('td[position()=1]/a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items  


##################### default parse province ######################
###########################   sample  #############################
#    def parse(self,response):
#        hxs=HtmlXPathSelector(response)
#        sites=hxs.select('//tr[@class=\'provincetr\']/td')
#        items=[]
#        global add
#        for site in sites:
#            add+=1
#            item=tongjiproItem()
#            item['id']=add
#            item['code']=site.select('a/@href').extract()
#            item['title']=site.select('a/text()').extract()
#            item['link'] = site.select('a/@href').extract()
#            item['addtime']=site.select('span/text()').extract()
#            items.append(item)
#        return items  
#####################  parse_item  ###############################


    def parse_item(self,response):
        item = tongjiproItem()
        sel = Selector(response)
        #sel = HtmlXPathSelector(response)
        #sel_t = Selector(text=response.body)

        global add
        print 'add= ',add
        add+=1

        item['id']=add
        #省(直辖市) >> 市(直辖区,) >> 区 >> 镇(街道) >> 村
        #provinces = sel.xpath('//tr[@class=\'provincetr\']/td[position()=1]/a/text()').extract()
        
        code = sel.xpath('//tr[@class=\'provincetr\']//td/a/@herf | //tr[@class=\'citytr\']/td[position()=1]/a/text() | //tr[@class=\'countytr\']/td[position()=1]/a/text() | //tr[@class=\'towntr\']/td[position()=1]/a/text() | //tr[@class=\'villagetr\']/td[position()=1]/text()').extract()
        item['code']=code and code[0] or ''
        
        title = sel.xpath('//tr[@class=\'provincetr\']//td/a/text() | //tr[@class=\'citytr\']/td[position()=2]/a/text() | //tr[@class=\'countytr\']/td[position()=2]/a/text() | //tr[@class=\'towntr\']/td[position()=2]/a/text() | //tr[@class=\'villagetr\']/td[position()=3]/text()').extract()
        item['title']=title and title[0] or ''
        
        item['link'] = response.url

        print item
        return item







