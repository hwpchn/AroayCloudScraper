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
