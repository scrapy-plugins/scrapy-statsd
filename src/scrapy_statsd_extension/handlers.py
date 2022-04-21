# -*- coding: utf-8 -*-
import statsd

from scrapy_statsd_extension import defaults, utils


class StatsdBase(object):
    def __init__(self, crawler_settings):
        host = crawler_settings.get("STATSD_HOST", defaults.STATSD_HOST)
        port = crawler_settings.get("STATSD_PORT", defaults.STATSD_PORT)
        prefix = crawler_settings.get("STATSD_PREFIX", defaults.STATSD_PREFIX)
        self.client = statsd.StatsClient(host, port, prefix)

        self.prefixes_to_log = crawler_settings.get(
            "STATSD_LOG_ONLY", defaults.STATSD_LOG_ONLY
        )
        self.log_all_fields = True

        self.ignored_prefixes = (
            crawler_settings.get("STATSD_IGNORE", defaults.STATSD_IGNORE) or []
        )

        self.tagging_enabled = crawler_settings.get(
            "STATSD_TAGGING", defaults.STATSD_TAGGING
        )
        self.tags = crawler_settings.get("STATSD_TAGS", defaults.STATSD_TAGS)

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def not_ignored_field(self, key):
        for prefix in self.ignored_prefixes:
            if key.startswith(prefix):
                return False
        return True

    def has_valid_prefix(self, key):
        if self.log_all_fields is True:
            return True

        for prefix in self.prefixes_to_log:
            if key.startswith(prefix):
                return True

        return False

    def get_tags(self, spider):
        if not self.tagging_enabled:
            return

        tags = {}

        if self.tags["spider_name_tag"]:
            tags["spider_name_tag"] = spider.name

        if hasattr("spider", "statsd_tags"):
            tags.extend(spider.statsd_tags)

        return tags

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.incr(key, value)
