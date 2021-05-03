import scrapy
from aroay_cloudscraper import CloudScraperRequest


class JavdbSpider(scrapy.Spider):
    name = 'javdb'
    allowed_domains = ['javdb.com']

    def start_requests(self):
        yield CloudScraperRequest("https://javdb.com/rankings/video_uncensored?period=daily", callback=self.parse,
                                  proxy={
                                      "http": "http://hwplargespeedproxies:EwftFeTD4QF4k0sZ@3.224.197.3:31112",
                                      "https": "http://hwplargespeedproxies:EwftFeTD4QF4k0sZ@3.224.197.3:31112"
                                  })

    def parse(self, response):
        print(response.text)
