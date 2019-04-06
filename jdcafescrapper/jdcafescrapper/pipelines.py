# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

class JdcafescrapperPipeline(object):
    def process_item(self, item, spider):
        return item

class CafeMongoPipeline:
   
    _cafe_mongo_collection = 'cafe_details'
    _cafe_url_collection = 'cafe_details_url'
   
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'cafelist':
            self.process_cafe_list(item)
        if spider.name == 'cafedetail':
            self.process_cafe_details(item)
        return item

    def process_cafe_list(self,item):
        #Verify if the item is already present.
        doc = self.db[self._cafe_mongo_collection].find_one({"docId":item['docId']})
        logging.info(doc)
        if  doc is None:
            #Save Cafe status doc in Mongo
            statusdoc = {"url":item['detailPgLnk'],"status":False,"docId":item['docId']}
            #Save Cafe detail page link in Mongo
            self.db[self._cafe_url_collection].insert_one(statusdoc)
            cafeDoc = dict(item)
            del cafeDoc['detailPgLnk']
            #Update cafe doc in Mongo
            self.db[self._cafe_mongo_collection].insert_one(cafeDoc)
        else:
            pass
    
    def process_cafe_details(self,item):
        if item is None:
            return item
        #Update Cafe Details in doc
        docId = item['docId']
        oldDoc = self.db[self._cafe_mongo_collection].find({"docId":docId})[0]
        logging.info(oldDoc)
        newDoc = { "$set": dict(item) }
        self.db[self._cafe_mongo_collection].update_one(oldDoc,newDoc)
        statusdoc = self.db[self._cafe_url_collection].find({"docId":docId})[0]
        #Update status
        statusnewDoc = { "$set": {"status":True} }
        self.db[self._cafe_url_collection].update_one(statusdoc,statusnewDoc)
