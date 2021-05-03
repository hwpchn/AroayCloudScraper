import scrapy
from aroay_cloudscraper import CloudScraperRequest


class JavdbSpider(scrapy.Spider):
    name = 'javdb'
    allowed_domains = ['javdb.com']

    def start_requests(self):
        yield CloudScraperRequest("https://javdb.com/rankings/video_uncensored?period=daily", callback=self.parse)

    def parse(self, response):
        print(response.text)
