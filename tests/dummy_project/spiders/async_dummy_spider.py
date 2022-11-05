# -*- coding: utf-8 -*-
import datetime as dt
import uuid

import scrapy


class DummySpiderSpider(scrapy.Spider):
    name = "async_dummy_spider"
    allowed_domains = ["example.com"]
    start_urls = ["http://example.com/"]

    async def parse(self, response):
        yield {
            "uuid": str(uuid.uuid1()),
            "timestamp": dt.datetime.now(),
            "url": response.url,
        }
