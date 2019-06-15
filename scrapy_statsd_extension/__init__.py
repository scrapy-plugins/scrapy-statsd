from scrapy_statsd_extension.utils import create_stat_key

import statsd
from scrapy import signals
from scrapy.exceptions import NotConfigured
from twisted.internet import task


class StatsdExtension(object):

    def __init__(self, crawler):
        if not crawler.settings.getbool('STATSD_ENABLED', True):
            raise NotConfigured

        host = crawler.settings.get('STATSD_HOST', 'localhost')
        port = crawler.settings.get('STATSD_PORT', 8125)

        self.log_periodic = crawler.settings.get('STATSD_LOG_PERIODIC', True)
        self.callack_timer = crawler.settings.get('STATSD_LOG_EVERY', 5)
        self.client = statsd.StatsClient(host, port)
        self.stats = crawler.stats
        self._last_stats = {}

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
                stat_key = create_stat_key(key)

                increment_amount = value - self._last_stats.get(stat_key, 0)
                self.client.incr(stat_key, increment_amount)

                self._last_stats[stat_key] = value

    def spider_closed(self, spider):
        if hasattr(self, 'log_task') and self.log_task.running:
            self.log_task.stop()

        self.log_stats(spider)
