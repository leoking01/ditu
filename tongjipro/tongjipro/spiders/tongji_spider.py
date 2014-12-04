#-*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from tongjipro.items import tongjiproItem
add = 0
class fjsenSpider(BaseSpider):
    name="tongji"
    allowed_domains=[]
    start_urls=['http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2013/index.html']
    #start_urls=['http://www.fjsen.com/j/node_94962_'+str(x)+'.htm' for x in range(2,11)]+['http://www.fjsen.com/j/node_94962.htm']

    def parse(self,response):
        hxs=HtmlXPathSelector(response)
        sites=hxs.select('//tr[@class=\'provincetr\']/td')
        items=[]
        global add

        for site in sites:
            add+=1
            item=tongjiproItem()
            item['id']=add
            item['title']=site.select('a/text()').extract()
            item['link'] = site.select('a/@href').extract()
            #item['link'] = site.response#select('a/@href').extract()
            item['addtime']=site.select('span/text()').extract()
            items.append(item)
        return items  



