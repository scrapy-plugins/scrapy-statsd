import statsd

from scrapy_statsd_extension import handlers


class GraphiteHandler(handlers.StatsdBaseHandler):
    def create_client(self, host, port, prefix):
        return statsd.StatsClient(host, port, prefix)

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.incr(key, value)
