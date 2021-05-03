import asyncio
import urllib
from functools import partial
import twisted.internet
import cloudscraper
from scrapy.http import HtmlResponse
from twisted.internet.asyncioreactor import AsyncioSelectorReactor
from twisted.internet.defer import Deferred
import sys

from .settings import *

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

reactor = AsyncioSelectorReactor(asyncio.get_event_loop())

# install AsyncioSelectorReactor
twisted.internet.reactor = reactor
sys.modules['twisted.internet.reactor'] = reactor


def as_deferred(f):
    """
    transform a Twisted Deffered to an Asyncio Future
    :param f: async function
    """
    return Deferred.fromFuture(asyncio.ensure_future(f))


logger = logging.getLogger('aroay_cloudscraper')


class CloudScraperMiddleware(object):
    """
    Downloader middleware handling the requests with Puppeteer
    """

    def __init__(self):
        self.scraper = cloudscraper.create_scraper(browser='chrome')

    # 将cloudflare变为协程函数
    def _block_get(self, url, *args, **kwargs):
        response = self.scraper.get(url, *args, **kwargs)
        # 返回response对象
        return response

    async def _simple_run_in_executor(self, f, *args, async_loop=None, **kwargs):
        loopx = async_loop or asyncio.get_event_loop()
        response = await loopx.run_in_executor(None, partial(f, *args, **kwargs))
        return response

    # f封装requests为协程函数
    async def async_get(self, url, *args, **kwargs):
        response = await self._simple_run_in_executor(self._block_get, url, *args, **kwargs)
        return response

    @classmethod
    def from_crawler(cls, crawler):
        """
        init the middleware
        :param crawler:
        :return:
        """
        settings = crawler.settings
        logging_level = settings.get('AROAY_CLOUDSCRAPER_LOGGING_LEVEL', AROAY_CLOUDSCRAPER_LOGGING_LEVEL)
        logging.getLogger('websockets').setLevel(logging_level)
        logging.getLogger('aroay_cloudscraper').setLevel(logging_level)
        cls.download_timeout = settings.get('AROAY_CLOUDSCRAPER_DOWNLOAD_TIMEOUT',
                                            settings.get('DOWNLOAD_TIMEOUT', AROAY_CLOUDSCRAPER_DOWNLOAD_TIMEOUT))
        cls.delay = settings.get('AROAY_CLOUDSCRAPER_DELAY', AROAY_CLOUDSCRAPER_DELAY)

        return cls()

    async def _process_request(self, request, spider):
        """
        use aroay_cloudscraper to process spider
        :param request:
        :param spider:
        :return:
        """
        # get aroay_cloudscraper meta
        cloudscraper_meta = request.meta.get('aroay_cloudscraper') or {}
        logger.debug('cloudscraper_meta %s', cloudscraper_meta)
        if not isinstance(cloudscraper_meta, dict) or len(cloudscraper_meta.keys()) == 0:
            return

        # 设置代理
        _proxy = cloudscraper_meta.get('proxy')
        logger.info("set proxy is %s" % _proxy)

        # 设置请求超时
        _timeout = self.download_timeout
        if cloudscraper_meta.get('timeout') is not None:
            _timeout = cloudscraper_meta.get('timeout')
        _headers = cloudscraper_meta.get('headers')
        _cookies = cloudscraper_meta.get('cookies ')

        logger.debug('crawling %s', request.url)

        response = await self.async_get(request.url, proxies=_proxy, timeout=_timeout, headers=_headers,
                                        cookies=_cookies)

        # 设置延迟
        _delay = self.delay
        if cloudscraper_meta.get('delay') is not None:
            _delay = cloudscraper_meta.get('delay')
        if _delay is not None:
            logger.debug('sleep for %ss', _delay)
            await asyncio.sleep(_delay)

        # 返回二进制
        response = HtmlResponse(
            request.url,
            status=response.status_code,
            headers=response.headers,
            body=response.content,
            encoding='utf-8',
            request=request
        )
        return response

    def process_request(self, request, spider):
        """
        process request using aroay_cloudscraper
        :param request:
        :param spider:
        :return:
        """
        logger.debug('processing request %s', request)
        return as_deferred(self._process_request(request, spider))

    async def _spider_closed(self):
        pass

    def spider_closed(self):
        """
        callback when spider closed
        :return:
        """
        return as_deferred(self._spider_closed())
