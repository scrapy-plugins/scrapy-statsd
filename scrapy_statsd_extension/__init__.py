import statsd
from scrapy import signals
from twisted.internet import task


class StatsdExtension(object):

    def __init__(self, crawler):
        host = crawler.settings.get('STATSD_HOST', 'localhost')
        port = crawler.settings.get('STATSD_PORT', 8125)

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
        self.task = task.LoopingCall(self.log_stats, spider)
        self.task.start(10)

    def log_stats(self, spider):
        for key, value in self.stats.get_stats().items():
            if isinstance(value, int) or isinstance(value, float):
                increment_amount = value - self._last_stats.get(key, 0)
                self.client.incr(key, increment_amount)

                self._last_stats[key] = value

    def spider_closed(self, spider):
        if self.task and self.task.running:
            self.task.stop()
