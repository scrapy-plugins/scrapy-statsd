# -*- coding: utf-8 -*-
from scrapy import signals
from scrapy.exceptions import NotConfigured
from scrapy.utils.misc import load_object
from twisted.internet.task import LoopingCall

from scrapy_statsd import defaults, utils


class StatsdExtension(object):
    def __init__(self, crawler):
        if not crawler.settings.getbool("STATSD_ENABLED", defaults.STATSD_ENABLED):
            raise NotConfigured

        self.log_periodic = crawler.settings.get(
            "STATSD_LOG_PERIODIC", defaults.STATSD_LOG_PERIODIC
        )
        self.callack_timer = crawler.settings.get(
            "STATSD_LOG_EVERY", defaults.STATSD_LOG_EVERY
        )

        self.handler = load_object(defaults.STATSD_HANDLER).from_crawler(crawler)
        self.stats = crawler.stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)

        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        if self.log_periodic:
            self.log_task = LoopingCall(self.log_stats, spider)
            self.log_task.start(self.callack_timer)

    def log_stats(self, spider):
        for key, value in self.stats.get_stats().items():
            if isinstance(value, int) or isinstance(value, float):
                self.handler.increment(utils.create_stat_key(key), value, spider)

    def spider_closed(self, spider):
        if hasattr(self, "log_task") and self.log_task.running:
            self.log_task.stop()

        self.log_stats(spider)
