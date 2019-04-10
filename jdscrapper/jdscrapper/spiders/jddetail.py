# -*- coding: utf-8 -*-
import scrapy
import logging
from scrapy.loader import ItemLoader
from jdscrapper.items import JDItem
import pymongo

class JDdetailSpider(scrapy.Spider):
    name = 'jddetail'
    _jd_url_collection = 'jd_details_url'
    retry_xpath = "//div[@id='setbackfix']"
    #allowed_domains = ['justdial.com']
    start_urls = []
    #custom_settings = {
    #    'FEED_URI':'/Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdscrapper/detail/jddetail.json'
    #}

    @classmethod
    def from_crawler(self, crawler, *args, **kwargs):
        logging.info("Inside Class Method")
        spider = super().from_crawler(crawler, *args, **kwargs)
        spider.start_urls = self.get_urls_from_mongo(self,crawler)
        return spider


    def parse(self, response):
        jdDetailSel = response.selector.xpath("//div[@id='setbackfix']")
        logging.info("Starting Detail Page Scrapping")
        openhours = []
        modesofpayment = []
        jditemloader = ItemLoader( item = JDItem(), selector=jdDetailSel, response=response)
        #Website Link
        jditemloader.add_xpath('website',"//div[contains(@class,'dtpage')]/div/div/ul/li/span/a[@rel='nofollow']/text()")
        #Average rating
        jditemloader.add_xpath('avgRating',"//div[@class='company-details']/div/div/div/span/span[@class='rating']/span/span[@class='value-titles']/text()")
        #Total Reviews
        jditemloader.add_xpath('totreviews',"//div[@class='company-details']/div/div/div/span/span/span[@class='votes']/text()")
        #doc Id of jd as per JD
        jditemloader.add_xpath('docId',"//form/input[@id='docid']/@value[1]")
        #Opening hours of jd
        openhours = self.parse_openhours(response)
        jditemloader.add_value('openhours',openhours)
       
        for quickInfoSel in response.selector.xpath("//body//div[contains(@class,'mreinfwpr')]"):
            logging.info(quickInfoSel)
            logging.info(quickInfoSel.xpath(".//p/text()"))
            #Modes of payment
            if quickInfoSel.xpath(".//p/text()").extract_first() is not None:
                if 'Payment' in quickInfoSel.xpath(".//p/text()").extract_first():
                    for mop in quickInfoSel.xpath(".//ul[@class='alstdul']/li/span[@class='lng_mdpay']/text()").extract():
                        modesofpayment.append(mop)
                    jditemloader.add_value('modesofpayment',modesofpayment)
                #Year of Establishment
                if 'Established' in quickInfoSel.xpath(".//p/text()").extract_first():
                     yearEst = str(quickInfoSel.xpath(".//ul[@class='alstdul']/li/text()").extract_first())
                     if type(yearEst) == str :
                        jditemloader.add_value('yearEst',yearEst)                  
        yield jditemloader.load_item()

    #Method to parse opening days and time of jd.
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
        url_collection = crawler.settings.get('DETAIL_URL_STATUS_COL')
        for url in self.db[url_collection].find({"status":False},{"url":1,"_id":0}):
            logging.info(url["url"][0])
            start_urls.append(url["url"][0])
        logging.info(self.start_urls)
        self.client.close()
        return start_urls
        
