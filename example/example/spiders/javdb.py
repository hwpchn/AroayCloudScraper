import scrapy
from aroay_cloudscraper import CloudScraperRequest


class JavdbSpider(scrapy.Spider):
    name = 'javdb'
    allowed_domains = ['javdb.com']
    headers = {"Accept-Language": "zh-cn;q=0.8,en-US;q=0.6"}

    def start_requests(self):
        yield CloudScraperRequest("https://javdb.com/v/BOeQO", callback=self.parse,headers=self.headers)

    def parse(self, response):
        print(response.text)
