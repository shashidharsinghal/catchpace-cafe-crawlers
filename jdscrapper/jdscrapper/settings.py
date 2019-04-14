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


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'jdscrapper (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 10
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'jsdcrapper.middlewares.JdscrapperSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
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
    #Privoxy
    #'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
    #'jdscrapper.middlewares.ProxyMiddleware': 100
}

ROTATING_PROXY_LIST_PATH = '/root/virtual_env/catchpace-cafe-crawlers/jdscrapper/freeproxylist.txt'

#ROTATING_PROXY_LIST = [
#        '207.182.135.123:8118',
#        '43.252.10.189:8080'
#        ]

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'jdscrapper.pipelines.JDMongoPipeline': 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
#FEED_URI="file:///Users/mmt5571/Documents/personal/study/udemy/virtual_workspace/jdscrapper/page1.csv"

#Mongo settings
MONGO_URI="mongodb+srv://catchpace:O01e2imlupSb8FQF@catchpace-db-mggdr.mongodb.net"
MONGO_DATABASE="jddata"
JD_ERROR_URL_COL="error_url"

#Cafe settings
INIT_REQ_URL="https://www.justdial.com/Gurgaon/Coffee-Shops-in-Gurgaon/nct-10104727/page-1"
DETAIL_DATA_COL="jd_details_cafe"
DETAIL_URL_STATUS_COL="jd_details_url_cafe"


#Library settings
#INIT_REQ_URL="https://www.justdial.com/Delhi/Libraries-in-Gurgaon/nct-10299414/page-1"
#DETAIL_DATA_COL="jd_details_lib"
#DETAIL_URL_COL="jd_details_url_lib"
