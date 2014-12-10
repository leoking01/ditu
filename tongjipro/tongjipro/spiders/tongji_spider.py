#-*- coding: utf-8 -*-
from urlparse import urljoin
from scrapy.http import Request

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector,Selector
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from tongjipro.items import tongjiproItem
import scrapy

import sys
import datetime
#import join
#add=0##province 的起点=0 总数31  净数=31
#add_ci = 31##city  的起点=31  累计总数376=31+8+337  总数337+8  净数=337  8市直辖市数的二倍,因为还有县
#add_cou =376 #county 的起点即累计数 376,净数=  1038
#add_t = 9246 ##town 的起点 1414  累计总数9246
#add_v = 13002 ##village 的起点 13002

sys.stdout = open('output.txt','w');
###########################################################  ditu start  ###################################################

#################### parse province ########################
#class provinceSpider(CrawlSpider):
class dituSpider(CrawlSpider):
    name="ditu"
    allowed_domains=['stats.gov.cn']
    start_urls=[
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/',
        ]  ##  province起点
    url_0 = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'


    def parse(self,response):
        sel=Selector(response)
        items = []
        #sites = sel.xpath('//tr[@class=\'provincetr\'] | //tr[@class=\'citytr\']|//tr[@class=\'countytr\'] |/tr[@class=\'towntr\']|tr[@class=\'villagetr\'] ')
        sites = sel.xpath('//tr[@class=\'provincetr\']')
        sites_t = sites.xpath('//td')
        ##项 item
        for site in sites_t:
            code=site.xpath('a/@href').extract()
            title=site.xpath('a/text()').extract()
            degree=1
            pcode=site.xpath('a/@href').extract()
            link=site.xpath('a/@href').extract()
            print '$$$$$$$ title=',title,' link=',link
            link='/'.join(link)
            link = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+link
            print 'newnewnew title=',title,' link=',link
            yield tongjiproItem(degree=degree,code=code,pcode=pcode,link=link,title=title)

        ##链接
        for sub_url in sites.xpath('//td/a/@href').extract():
            url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+ str(sub_url)
            print '999999========= url= ',url
            yield scrapy.Request(url, callback=self.parse)




#            codes = sel.xpath('//tr[@class=\'provincetr\']//td/a/@herf | //tr[@class=\'citytr\']/td[position()=1]/a/text() | //tr[@class=\'countytr\']/td[position()=1]/a/text() | //tr[@class=\'towntr\']/td[position()=1]/a/text() | //tr[@class=\'villagetr\']/td[position()=1]/text()').extract()
#            titles = sel.xpath('//tr[@class=\'provincetr\']//td/a/text() | //tr[@class=\'citytr\']/td[position()=2]/a/text() | //tr[@class=\'countytr\']/td[position()=2]/a/text() | //tr[@class=\'towntr\']/td[position()=2]/a/text() | //tr[@class=\'villagetr\']/td[position()=3]/text()').extract()
#            links = sel.xpath('//tr[@class=\'provincetr\']//td/a/@href | //tr[@class=\'citytr\']/td[position()=1]/a/@href | //tr[@class=\'countytr\']/td[position()=1]/a/@href | //tr[@class=\'towntr\']/td[position()=1]/a/@href | //tr[@class=\'villagetr\']/td[position()=1]/@href ').extract()
#        for site in sites:
#            item=tongjiproItem()
#            add+=1
#            item['id']=add
#            item['code']=site.select('a/@href').extract()
#            item['title']=site.select('a/text()').extract()
#            item['link']=site.select('a/@href').extract()
#            item['addtime']=site.select('a/@href').extract()
#            items.append(item)
        #collect `item_urls`
        #for item_url in item_urls:
        #    yield Request(url=item_url, callback=self.parse_item)
#        return items

#            code = sel.xpath('//tr[@class=\'provincetr\']//td/a/@herf | //tr[@class=\'citytr\']/td[position()=1]/a/text() | //tr[@class=\'countytr\']/td[position()=1]/a/text() | //tr[@class=\'towntr\']/td[position()=1]/a/text() | //tr[@class=\'villagetr\']/td[position()=1]/text()').extract()
#            title = sel.xpath('//tr[@class=\'provincetr\']//td/a/text() | //tr[@class=\'citytr\']/td[position()=2]/a/text() | //tr[@class=\'countytr\']/td[position()=2]/a/text() | //tr[@class=\'towntr\']/td[position()=2]/a/text() | //tr[@class=\'villagetr\']/td[position()=3]/text()').extract()
#            link=sel.xpath('//tr[@class=\'provincetr\']//td/a/@href | //tr[@class=\'citytr\']/td[position()=1]/a/@href | //tr[@class=\'countytr\']/td[position()=1]/a/text() | //tr[@class=\'towntr\']/td[position()=1]/a/@href | //tr[@class=\'villagetr\']/td[position()=1]/@href ').extract()

##########################################################   ditu finish ###############################################

##################### parse city  ######################
class citySpider(CrawlSpider):
    name="city"
    allowed_domains=['stats.gov.cn']
    ##city起点.参数x.
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
    ##需要修改y
    start_urls=[
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(x)+'0'+str(y)+'.html' and\
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(x)+str(y1)+'.html'\
        #for x in range(10,66)for y in range(0,9) for y1 in range(9,40)
        for x in range(10,66)for y in range(0,1) for y1 in range(9,11)
    ] ##city 起点
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
    ##需要修改z
    start_urls=[
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+str(x)+'0'+str(y1)+'0'+str(z1)+'.html'and\
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+str(x)+str(y2)+'0'+str(z1)+'.html' and\
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+str(x)+'0'+str(y1)+str(z2)+'.html'and\
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+str(x)+str(y2)+str(z2)+'.html'\
        for x in range(11,66) for y1 in range(0,1)for z1 in range(0,1)  for y2 in range(9,11)  for z2 in range(9,11)
        #for x in range(11,66) for y1 in range(0,9)for z1 in range(0,9)  for y2 in range(9,35)  for z2 in range(9,35)
        #for x in range(11,66) for y1 in range(0,9)for z1 in range(0,9)  for y2 in range(9,25)  for z2 in range(25,35)
        #for x in range(11,66) for y1 in range(0,9)for z1 in range(0,9)  for y2 in range(25,35)  for z2 in range(9,25)
        #for x in range(11,66) for y1 in range(0,9)for z1 in range(0,9)  for y2 in range(25,35)  for z2 in range(25,35)
    ] 

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
    ##需要修改u
    start_urls=[
        ##111
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+'0'+str(z1)+'/'+str(x)+'0'+str(y1)+'0'+str(z1)+'0'+str(u1)+'.html' and \
        ##211
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+'0'+str(z1)+'/'+str(x)+str(y2)+'0'+str(z1)+'0'+str(u1)+'.html' and \
        ##121
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+str(z2)+'/'+str(x)+'0'+str(y1)+str(z2)+'0'+str(u1)+'.html' and \
        ##221
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+str(z2)+'/'+str(x)+str(y2)+str(z2)+'0'+str(u1)+'.html' and  \
        ##112
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+'0'+str(z1)+'/'+str(x)+'0'+str(y1)+'0'+str(z1)+str(u2)+'.html'and \
        ##212
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+'0'+str(z1)+'/'+str(x)+str(y2)+'0'+str(z1)+str(u2)+'.html'  \
        ##122
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+'0'+str(y1)+'/'+str(z2)+'/'+str(x)+'0'+str(y1)+str(z2)+str(u2)+'.html'  \
        ##222
        'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/'+str(x)+'/'+str(y2)+'/'+str(z2)+'/'+str(x)+str(y2)+str(z2)+str(u2)+'.html'  \
        #for x in range(11,66) for y1 in range(0,9)for z1 in range(0,9)for u1 in range(0,9)for y2 in range(9,15)for z2 in range(9,15)for u2 in range(9,15)
        for x in range(11,66) for y1 in range(0,1)for z1 in range(0,1)for u1 in range(0,1)for y2 in range(9,11)for z2 in range(9,11)for u2 in range(9,11)

    ] 

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







