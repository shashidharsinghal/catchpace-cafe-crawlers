# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from jdscrapper.items import JDItem
import logging

class JDlistSpider(scrapy.Spider):
    #Identity
    name = 'jdlist'
    retry_xpath = "//li[@class='cntanr']"
    #custom_settings = {
    #    'FEED_URI':'/Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdscrapper/listing/jdlist.json'
    #}
    #allowed_domains = ['justdial.com']
    firstelement = True

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.start_urls.append(crawler.settings.get('INIT_REQ_URL'))
        return spider

    def parse(self, response):
        for jd in response.selector.xpath("//li[@class='cntanr']"):
            loader = ItemLoader( item = JDItem(), selector = jd, response = response )
            #Name of the jd
            loader.add_xpath('name',".//section/div/section[@class='jcar']/div/h2/span/a/span/text()[1]")
            #Address of the jd
            loader.add_xpath('addr',".//section/div/section[@class='jcar']/div/p[3]/span/a/span[2]/span[@class='cont_fl_addr']/text()[1]")
            #Reviews count 
            #loader.add_xpath('revCount',".//section/div/section[@class='jcar']/div/p[1]/a/span[@class='rt_count lng_vote']/text()[1]")
            #Detail page link
            loader.add_xpath('detailPgLnk',".//span[@class='jcn']/a/@href")
            #Doc ID of jd as per JD
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
