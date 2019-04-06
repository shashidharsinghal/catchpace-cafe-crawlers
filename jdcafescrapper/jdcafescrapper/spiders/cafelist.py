# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from jdcafescrapper.items import CafeItem
import logging

class CafelistSpider(scrapy.Spider):
    #Identity
    name = 'cafelist'
    retry_xpath = "//li[@class='cntanr']"
    #custom_settings = {
    #    'FEED_URI':'/Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdcafescrapper/listing/cafelist.json'
    #}
    #allowed_domains = ['justdial.com']
    start_urls = ['https://www.justdial.com/Gurgaon/Coffee-Shops-in-Gurgaon/nct-10104727/page-1']
    firstelement = True

    def parse(self, response):
        for cafe in response.selector.xpath("//li[@class='cntanr']"):
            loader = ItemLoader( item = CafeItem(), selector = cafe, response = response )
            #Name of the Cafe
            loader.add_xpath('name',".//section/div/section[@class='jcar']/div/h2/span/a/span/text()[1]")
            #Address of the Cafe
            loader.add_xpath('addr',".//section/div/section[@class='jcar']/div/p[3]/span/a/span[2]/span[@class='cont_fl_addr']/text()[1]")
            #Reviews count 
            #loader.add_xpath('revCount',".//section/div/section[@class='jcar']/div/p[1]/a/span[@class='rt_count lng_vote']/text()[1]")
            #Detail page link
            loader.add_xpath('detailPgLnk',".//span[@class='jcn']/a/@href")
            #Doc ID of cafe as per JD
            loader.add_xpath('docId',".//span[@class='jcn']/a/@onclick")
            #PhoneNumber
            if self.firstelement:
                loader.add_xpath('phoneNumber',".//section/div/section[@class='jcar']/div/p/span/a/b/span[@class]/@class")
                self.firstelement = False
            else:
                loader.add_xpath('phoneNumber',".//section/div/section[@class='jcar']/div/p/span/a/span[contains(@class,'mobilesv')]/@class")
            #Flag to keep track if the details page is crawled
            #loader.add_value('dtlsPgSuccess',False)
            yield loader.load_item()
            
        next_page = response.selector.xpath("//a[@rel='next']/@href").extract_first()
        
        #Crawl to the end of the page.
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            logging.info(next_page_link)
            yield scrapy.Request(url=next_page_link,callback=self.parse)
