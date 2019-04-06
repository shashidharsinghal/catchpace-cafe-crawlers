# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from jdcafescrapper.items import CafeItem
import pymongo

class CafedetailSpider(scrapy.Spider):
    name = 'cafedetail'
    _cafe_url_collection = 'cafe_details_url'
    retry_xpath = "//div[@id='setbackfix']"
    #allowed_domains = ['justdial.com']
    start_urls = []
    #custom_settings = {
    #    'FEED_URI':'/Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdcafescrapper/detail/cafedetail.json'
    #}

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        logging.info("Inside Class Method")
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.start_urls = self.get_urls_from_mongo(self,crawler)
        return spider


    def parse(self, response):
        cafeDetailSel = response.selector.xpath("//div[@id='setbackfix']")
        logging.info("Starting Detail Page Scrapping")
        openhours = []
        cafeitemloader = ItemLoader( item = CafeItem(), selector=cafeDetailSel, response=response)
        #Website Link
        cafeitemloader.add_xpath('website',"//div[contains(@class,'dtpage')]/div/div/ul/li/span/a[@rel='nofollow']/text()")
        #Average rating
        cafeitemloader.add_xpath('avgRating',"//div[@class='company-details']/div/div/div/span/span[@class='rating']/span/span[@class='value-titles']/text()")
        #Total Reviews
        cafeitemloader.add_xpath('totreviews',"//div[@class='company-details']/div/div/div/span/span/span[@class='votes']/text()")
        #doc Id of cafe as per JD
        cafeitemloader.add_xpath('docId',"//form/input[@id='docid']/@value[1]")
        #Opening hours of cafe
        openhours = self.parse_openhours(response)
        cafeitemloader.add_value('openhours',openhours)
        yield cafeitemloader.load_item()
    
    #Method to parse opening days and time of cafe.
    def parse_openhours(self,response):
        openhours = []
        for openHr in response.selector.xpath("//div[contains(@class,'dtpage')]/div/div/ul[@id='statHr']/li"):
            openHour = {}
            day = openHr.xpath(".//span[contains(@class,'1')]/text()[1]").extract_first()
            timestr = openHr.xpath(".//span[contains(@class,'2')]/text()[1]").extract_first()
            time = [x.strip() for x in timestr.split('-')]
            if len(time) > 1: 
                openHour["day"] = day
                openHour["open"] = time[0]
                openHour["close"] = time[1]
                openhours.append(openHour)
        return openhours

    def get_urls_from_mongo(self,crawler):
        #Get Mongo connection
        start_urls = []
        logging.info("Fetching urls from Mongo DB")
        self.client = pymongo.MongoClient(crawler.settings.get('MONGO_URI'))
        self.db = self.client[crawler.settings.get('MONGO_DATABASE')]
        for url in self.db[self._cafe_url_collection].find({"status":False},{"url":1,"_id":0}):
            logging.info(url["url"][0])
            start_urls.append(url["url"][0])
        logging.info(self.start_urls)
        self.client.close()
        return start_urls
        
