# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import logging

class JdscrapperPipeline(object):
    def process_item(self, item, spider):
        return item

class JDMongoPipeline:
   
    def __init__(self, mongo_uri, mongo_db,jd_data_collection,jd_data_url_collection):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.jd_data_collection =  jd_data_collection
        self.jd_data_url_collection = jd_data_url_collection

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            jd_data_collection=crawler.settings.get('DETAIL_DATA_COL'),
            jd_data_url_collection=crawler.settings.get('DETAIL_URL_STATUS_COL'),
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if spider.name == 'jdlist':
            self.process_jd_list(item)
        if spider.name == 'jddetail':
            self.process_jd_details(item)
        return item

    def process_jd_list(self,item):
        #Verify if the item is already present.
        doc = self.db[self.jd_data_collection].find_one({"docId":item['docId']})
        logging.info(doc)
        if  doc is None:
            #Save JD status doc in Mongo
            statusdoc = {"url":item['detailPgLnk'],"status":False,"docId":item['docId']}
            #Save JD detail page link in Mongo
            self.db[self.jd_data_url_collection].insert_one(statusdoc)
            jdDoc = dict(item)
            del jdDoc['detailPgLnk']
            #Update jd doc in Mongo
            self.db[self.jd_data_collection].insert_one(jdDoc)
        else:
            pass
    
    def process_jd_details(self,item):
        if item is None:
            return item
        #Update jd Details in doc
        docId = item['docId']
        oldDoc = self.db[self.jd_data_collection].find({"docId":docId})[0]
        logging.info(oldDoc)
        newDoc = { "$set": dict(item) }
        self.db[self.jd_data_collection].update_one(oldDoc,newDoc)
        statusdoc = self.db[self.jd_data_url_collection].find({"docId":docId})[0]
        #Update status
        statusnewDoc = { "$set": {"status":True} }
        self.db[self.jd_data_url_collection].update_one(statusdoc,statusnewDoc)
