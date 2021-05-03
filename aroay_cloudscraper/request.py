from scrapy import Request
import copy


class CloudScraperRequest(Request):
    """
    Scrapy ``Request`` subclass providing additional arguments
    """

    def __init__(self, url, callback=None, proxy: dict = None, headers=None,
                 delay=None, timeout=None, meta=None, *args, cookies=None,
                 **kwargs):
        """
        :param url: request url
        :param callback: callback
        :param proxy: use proxy for this time, like `http://x.x.x.x:x`
        :param sleep: time to sleep after loaded, override `AROAY_CLOUDSCRAPER_SLEEP`
        :param timeout: load timeout, override `AROAY_CLOUDSCRAPER_DOWNLOAD_TIMEOUT`
        :param args:
        :param kwargs:
        """
        # use meta info to save args
        meta = copy.deepcopy(meta) or {}
        cloudscraper_meta = meta.get('aroay_cloudscraper') or {}
        self.delay = cloudscraper_meta.get('delay') if cloudscraper_meta.get('delay') is not None else delay
        self.proxy = cloudscraper_meta.get('proxy') if cloudscraper_meta.get('proxy') is not None else proxy
        self.timeout = cloudscraper_meta.get('timeout') if cloudscraper_meta.get('timeout') is not None else timeout
        self.headers = cloudscraper_meta.get('headers') if cloudscraper_meta.get('headers') is not None else headers
        self.cookies = cloudscraper_meta.get('cookies') if cloudscraper_meta.get('cookies') is not None else cookies
        cloudscraper_meta = meta.setdefault('aroay_cloudscraper', {})
        cloudscraper_meta['proxy'] = self.proxy
        cloudscraper_meta['delay'] = self.delay
        cloudscraper_meta['timeout'] = self.timeout
        cloudscraper_meta['headers'] = self.headers
        cloudscraper_meta['cookies'] = self.cookies

        super().__init__(url, callback, meta=meta, *args, **kwargs)
