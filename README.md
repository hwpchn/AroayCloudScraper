# AroayCloudScraper
scrapy一个插件，绕过cloudflare检测，主要是封装 cloudscraper模块

# 需setting设置

```
# 默认日志级别
AROAY_CLOUDSCRAPER_LOGGING_LEVEL = logging.DEBUG

默认超时
AROAY_CLOUDSCRAPER_DOWNLOAD_TIMEOUT = 30

# 默认延迟
AROAY_CLOUDSCRAPER_DELAY = 1

#必须设置，否则报错
COMPRESSION_ENABLED = False
```

# 代理使用

```
    def start_requests(self):
        for page in range(1, 2):
            yield CloudScraperRequest(self.base_url, callback=self.parse_index, dont_filter=True, proxy={
                "http": "http://username:password@ip:port",
                "https": "http://username:password@ip:port",
            },cookies={"over18":"1"},timeout=5)
```
