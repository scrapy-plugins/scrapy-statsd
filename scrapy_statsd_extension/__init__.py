from scrapy_statsd_extension import utils, defaults

import statsd
from scrapy import signals
from scrapy.exceptions import NotConfigured
from twisted.internet import task


class StatsdExtension(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('STATSD_ENABLED', defaults.STATSD_ENABLED):
            raise NotConfigured

        host = crawler.settings.get('STATSD_HOST', defaults.STATSD_HOST)
        port = crawler.settings.get('STATSD_PORT', defaults.STATSD_PORT)

        self.log_periodic = crawler.settings.get(
            'STATSD_LOG_PERIODIC', defaults.STATSD_LOG_PERIODIC)
        self.callack_timer = crawler.settings.get(
            'STATSD_LOG_EVERY', defaults.STATSD_LOG_EVERY)
        self.client = statsd.StatsClient(host, port)
        self.stats = crawler.stats

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler)

        crawler.signals.connect(
            ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(
            ext.spider_closed, signal=signals.spider_closed)

        return ext

    def spider_opened(self, spider):
        if self.log_periodic:
            self.log_task = task.LoopingCall(self.log_stats, spider)
            self.log_task.start(self.callack_timer)

    def log_stats(self, spider):
        for key, value in self.stats.get_stats().items():
            if isinstance(value, int) or isinstance(value, float):
                stat_key = utils.create_stat_key(key)
                self.client.incr(stat_key, value)

    def spider_closed(self, spider):
        if hasattr(self, 'log_task') and self.log_task.running:
            self.log_task.stop()

        self.log_stats(spider)
