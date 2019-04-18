# -*- coding: utf-8 -*-
import scrapy
from scrapy.loader import ItemLoader
from jdscrapper.items import JDItem
import logging
from scrapy.http.request import Request

class JDlistSpider(scrapy.Spider):
    #Identity
    name = 'jdlist'
    retry_xpath = "//li[@class='cntanr']"
    #custom_settings = {
    #    'FEED_URI':'/Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdscrapper/listing/jdlist.json'
    #}
    #allowed_domains = ['justdial.com']
    firstelement = True
    req_urls = []


    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.req_urls.append(crawler.settings.get('INIT_REQ_URL'))
        return spider

    def start_requests(self):
        for url in self.req_urls:
            logging.info(self.req_urls)
            #self.executeRequest(url) 
            yield Request(url,
                 meta = {
                     'dont_redirect': True,
                      'handle_httpstatus_list': [301,302]
                  },
                  callback= self.parse)


    def parse(self, response):
        for jd in response.selector.xpath("//li[@class='cntanr']"):
            loader = ItemLoader( item = JDItem(), selector = jd, response = response )
            #Name of the jd
            loader.add_xpath('name',".//section/div/section[@class='jcar']/div/h2/span/a/span/text()[1]")
            #Address of the jd
            loader.add_xpath('addr',".//section/div/section[@class='jcar']/div/p[3]/span/a/span[2]/span[@class='cont_fl_addr']/text()[1]")
            #Detail page link
            loader.add_xpath('detailPgLnk',".//span[@class='jcn']/a/@href")
            #Doc ID of jd as per JD
            loader.add_xpath('docId',".//span[@class='jcn']/a/@onclick")
            #PhoneNumber
            phone_number_xpath_1 = ".//section/div/section[@class='jcar']/div/p/span/a/b/span[@class]/@class"
            phone_number_xpath_2 = ".//section/div/section[@class='jcar']/div/p/span/a/span[contains(@class,'mobilesv')]/@class"
            logging.info(jd.xpath(phone_number_xpath_1).extract())
            if jd.xpath(phone_number_xpath_1).extract_first() is not None:
                logging.info("Fetching phone number from xpath 1.")
                loader.add_xpath('phoneNumber',phone_number_xpath_1)
            else:
                logging.info("Fetching phone number from xpath 2.")
                logging.info(jd.xpath(phone_number_xpath_2).extract())
                loader.add_xpath('phoneNumber',phone_number_xpath_2)
            yield loader.load_item()
            
        next_page = response.selector.xpath("//a[@rel='next']/@href").extract_first()
        
        #Crawl to the end of the page.
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            logging.info(next_page_link)
            #self.executeRequest(next_page_link)
            yield scrapy.Request(url=next_page_link,
                  meta = {
                      'dont_redirect': True,
                      'handle_httpstatus_list': [301,302]
                    },
                    callback=self.parse)
