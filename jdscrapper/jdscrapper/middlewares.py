# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random, logging
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from scrapy.http import headers
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
import pymongo
import logging

class UserAgentRotatorMiddleware(UserAgentMiddleware):

    user_agents_list = [
    # Google Chrome
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1290.1 Safari/537.13",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.13 (KHTML, like Gecko) Chrome/24.0.1284.0 Safari/537.13",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.6 Safari/537.11",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.17 Safari/537.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_0) AppleWebKit/537.4 (KHTML, like Gecko) Chrome/22.0.1229.79 Safari/537.4",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    # FireFox
    "Mozilla/5.0 (Windows NT 6.1; rv:15.0) Gecko/20120716 Firefox/15.0a2",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.16) Gecko/20120427 Firefox/15.0a1",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:14.0) Gecko/20120405 Firefox/14.0a1",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:14.0) Gecko/20100101 Firefox/14.0.1",
    "Mozilla/5.0 (Windows NT 6.0; rv:14.0) Gecko/20100101 Firefox/14.0.1",
    "Mozilla/5.0 (Windows NT 5.1; rv:15.0) Gecko/20100101 Firefox/13.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.1.16) Gecko/20120421 Gecko Firefox/11.0",
    "Mozilla/5.0 (Windows NT 5.1; rv:12.0) Gecko/20120403211507 Firefox/12.0",
    "Mozilla/5.0 (Windows NT 6.1; U;WOW64; de;rv:11.0) Gecko Firefox/11.0",
    # Safari
    "Mozilla/5.0 (iPad; CPU OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5355d Safari/8536.25",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/537.13+ (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/534.55.3 (KHTML, like Gecko) Version/5.1.3 Safari/534.53.10",
    "Mozilla/5.0 (iPad; CPU OS 5_1 like Mac OS X) AppleWebKit/534.46 (KHTML, like Gecko ) Version/5.1 Mobile/9B176 Safari/7534.48.3",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; de-at) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_7; da-dk) AppleWebKit/533.21.1 (KHTML, like Gecko) Version/5.0.5 Safari/533.21.1",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; tr-TR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; ko-KR) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    "Mozilla/5.0 (Windows; U; Windows NT 6.1; cs-CZ) AppleWebKit/533.20.25 (KHTML, like Gecko) Version/5.0.4 Safari/533.20.27",
    # Opera
    "Opera/9.80 (Windows NT 6.1; U; es-ES) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 5.1; U; zh-sg) Presto/2.9.181 Version/12.00",
    "Opera/9.80 (Windows NT 6.1; WOW64; U; pt) Presto/2.10.229 Version/11.62",
    "Opera/9.80 (Windows NT 6.0; U; pl) Presto/2.10.229 Version/11.62",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; de) Presto/2.9.168 Version/11.52",
    "Opera/9.80 (Windows NT 5.1; U; en) Presto/2.9.168 Version/11.51",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; de) Opera 11.51",
    "Opera/9.80 (X11; Linux x86_64; U; fr) Presto/2.9.168 Version/11.50",
    "Opera/9.80 (X11; Linux i686; U; ru) Presto/2.8.131 Version/11.11",
    # Internet Explorer
    "Mozilla/5.0 (compatible; MSIE 10.6; Windows NT 6.1; Trident/5.0; InfoPath.2; SLCC1; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET CLR 2.0.50727) 3gpp-gba UNTRUSTED/1.0",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/4.0; InfoPath.2; SV1; .NET CLR 2.0.50727; WOW64)",
    "Mozilla/5.0 (compatible; MSIE 10.0; Macintosh; Intel Mac OS X 10_7_3; Trident/6.0)",
    "Mozilla/4.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/5.0)",
    "Mozilla/1.22 (compatible; MSIE 10.0; Windows 3.1)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; WIndows NT 9.0; en-US))",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
]

    def __init__(self,user_agent=''):
        self.user_agent = user_agent
    def process_request(self, request, spider):
        try:  
            self.user_agent = random.choice(self.user_agents_list)
            request.headers.setdefault('User-Agent',self.user_agent)
        except IndexError:
            logging.error('Error in getting user Agent')



class JdscrapperSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JdscrapperDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class JDRetryMiddleware(RetryMiddleware):

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response
        if response.status in self.retry_http_codes:
            reason = response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        
        # continue
        if 'robots' not in request.url and len(response.xpath(spider.retry_xpath))==0:
            return self._retry(request, 'response got xpath "{}"'.format(spider.retry_xpath), spider) or response
        
        return response

from stem import Signal
from stem.control import Controller
from toripchanger import TorIpChanger

# A Tor IP will be reused only after 10 different IPs were used.
#ip_changer = TorIpChanger(tor_password='shashitor',tor_port='9051',local_http_proxy='http://127.0.0.1:8118')



def _set_new_ip():
      with Controller.from_port(port=9051) as controller:
        controller.authenticate(password='shashitor')
        controller.signal(Signal.NEWNYM)

class ProxyMiddleware(object):
    #_req_count=0
    #ip_changer.get_new_ip()

    #def _set_new_ip():
     # with Controller.from_port(port=9051) as controller:
      #  controller.authenticate(password='shashitor')
       # controller.signal(Signal.NEWNYM)

    def process_request(self, request, spider):
        #self._req_count +=1
        #if self._req_count > 10:
        #    self._req_count=0
        #    ip_changer.get_new_ip()
        _set_new_ip()
        request.meta['proxy'] = 'http://127.0.0.1:8118'
        spider.log('Proxy : %s' % request.meta['proxy'])
