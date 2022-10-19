# -*- coding: utf-8 -*-
STATSD_ENABLED = False
STATSD_HOST = "localhost"
STATSD_PORT = 8125
STATSD_LOG_PERIODIC = True
STATSD_LOG_EVERY = 5
STATSD_HANDLER = "scrapy_statsd.handlers.StatsdBase"
STATSD_PREFIX = "scrapy"
STATSD_LOG_ONLY = []
STATSD_TAGGING = False
STATSD_TAGS = {"spider_name": True}
STATSD_IGNORE = []
