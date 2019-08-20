import statsd

from scrapy_statsd_extension import utils, defaults


class StatsdBase(object):

    def __init__(self, host, port, prefix, log_only, ignored_prefixes):
        self.client = statsd.StatsClient(host, port, prefix)

        self.dont_log_all_fields = bool(log_only) 
        if self.dont_log_all_fields:
            self.prefixes_to_log = log_only

        self.ignored_prefixes = ignored_prefixes or []

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get('STATSD_HOST', defaults.STATSD_HOST)
        port = crawler.settings.get('STATSD_PORT', defaults.STATSD_PORT)
        prefix = crawler.settings.get('STATSD_PREFIX', defaults.STATSD_PREFIX)
        log_only = crawler.settings.get('STATSD_LOG_ONLY', defaults.STATSD_LOG_ONLY)
        ignored_prefixes = crawler.settings.get('STATSD_IGNORE', defaults.STATSD_IGNORE)

        return cls(host, port, prefix, log_only, ignored_prefixes)

    def not_ignored_field(self, key):
        for prefix in self.ignored_prefixes:
            if key.startswith(prefix):
                return False

        return True

    def has_valid_prefix(self, key):
        if self.dont_log_all_fields is False:
            return True

        for prefix in self.prefixes_to_log:
            if key.startswith(prefix):
                return True

        return False

    def increment(self, key, value):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.incr(key, value)
