# coding=utf-8

from scrapy.http import HtmlResponse
from selenium import webdriver
# from urlparse import urlparse

from andromeda import settings
import logging


class PhantomJSDownloader(object):

    def process_request(self, request, spider):
        response    = None
        if spider.name in settings.PHANTOMJS_SPIDER:
            browser = webdriver.PhantomJS(executable_path=settings.PHANTOMJS_PATH)
            try:
                browser.set_window_size(1024, 768)
                browser.get(request.url)
                content     = browser.page_source.encode("utf-8")
                url         = browser.current_url.encode('utf-8')
                response = HtmlResponse(url, encoding='utf-8', status=200, body=content)
            except Exception as e:
                logging.error(e.message)
            finally:
                browser.close()
            return response


    def process_response(self, request, response, spider):
        return response


