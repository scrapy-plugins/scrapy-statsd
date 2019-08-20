import statsd

from scrapy_statsd_extension import utils, defaults


class StatsdBase(object):

    def __init__(self, host, port, prefix):
        self.client = statsd.StatsClient(host, port, prefix)

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('STATSD_HOST', defaults.STATSD_HOST)
        port = crawler.settings.get('STATSD_PORT', defaults.STATSD_PORT)
        prefix = crawler.settings.get('STATSD_PREFIX', defaults.STATSD_PREFIX)

        return cls(host, port, prefix)

    def increment(self, key, value):
        self.client.incr(key, value)
