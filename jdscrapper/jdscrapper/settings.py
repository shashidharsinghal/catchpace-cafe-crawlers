# -*- coding: utf-8 -*-

# Scrapy settings for jdscrapper project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'jdscrapper'

SPIDER_MODULES = ['jdscrapper.spiders']
NEWSPIDER_MODULE = 'jdscrapper.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
RETRY_HTTP_CODES = [301,302]

DOWNLOAD_DELAY = 2
RETRY_TIMES = 50
ROTATING_PROXY_PAGE_RETRY_TIMES = 50
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

DOWNLOADER_MIDDLEWARES = {
    #Random User-Agent    
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'jdscrapper.middlewares.UserAgentRotatorMiddleware': 400,
    #Retry Middleware
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    'jdscrapper.middlewares.JDRetryMiddleware': 500,
    #Rotating proxy Middleware
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    #Ban Detection Middleware
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620
}
ROTATING_PROXY_BACKOFF_BASE = 30
ROTATING_PROXY_LIST_PATH = '/root/virtual_env/catchpace-cafe-crawlers/jdscrapper/freeproxylist.txt'
#ROTATING_PROXY_LIST_PATH = '/Users/mmt5571/Documents/personal/study/catchpace/virtual_workspace/catchpace-cafe-crawlers/jdscrapper/freeproxylist.txt'

#ROTATING_PROXY_LIST = [
#       '185.130.144.241:3004'
#      ]

#Cities To Scrap
LIST_CITIES = ['Delhi','Gurgaon','Bangalore','Mumbai','Chennai','Dehradun','Noida','Faridabad','Pune','Meerut','Kanpur',
    'Jaipur','Ahemdabad','Hyderabad','Surat','Kolkata','Kota','Lucknow','Indore','Bhopal','Chittoor','Nagpur','Chandigarh',
    'Guwahati'
]

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'jdscrapper.pipelines.JDMongoPipeline': 300,
}

AUTOTHROTTLE_ENABLED = True

#Mongo settings
MONGO_URI="mongodb+srv://catchpace:O01e2imlupSb8FQF@catchpace-db-mggdr.mongodb.net"
MONGO_DATABASE="jddatacty"
JD_ERROR_URL_COL="error_url"

#Cafe settings
#INIT_REQ_URL="https://www.justdial.com/Gurgaon/Coffee-Shops-in-Gurgaon/nct-10104727/page-40"
#DETAIL_DATA_COL="jd_details_cafe"
#DETAIL_URL_STATUS_COL="jd_details_url_cafe"


#Library settings
INIT_REQ_URL="https://www.justdial.com/Delhi/Libraries-in-Gurgaon/page-49"
DETAIL_DATA_COL="jd_details_lib"
DETAIL_URL_STATUS_COL="jd_details_url_lib"

#Setting up logging properties
import logging
from logging.handlers import RotatingFileHandler

from scrapy.utils.log import configure_logging

LOG_ENABLED = True
# Disable default Scrapy log settings.
configure_logging(install_root_handler=True)

# Define your logging settings.
log_file = '/root/virtual_env/catchpace-cafe-crawlers/jdscrapper/jdlogs.log'
#log_file = '/Users/mmt5571/Documents/personal/study/catchpace/virtual_workspace/catchpace-cafe-crawlers/jdscrapper/jdlogs.log'

root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
rotating_file_log = RotatingFileHandler(log_file, maxBytes=10485760, backupCount=1)
rotating_file_log.setLevel(logging.INFO)
rotating_file_log.setFormatter(formatter)
root_logger.addHandler(rotating_file_log)

