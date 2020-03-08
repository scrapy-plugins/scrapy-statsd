import statsd

from scrapy_statsd_extension.handlers import StatsdBaseHandler


class TelegrafHandler(StatsdBaseHandler):
    def create_client(self, host, port, prefix):
        return statsd.StatsClient(host, port, prefix)

    def get_formatted_tags(self, spider):
        tags = self.get_tags(spider)
        return [f"{key}={value}" for key, value in tags.items()]

    def increment(self, key, value, spider):
        formatted_tags = self.get_formatted_tags(spider)

        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.incr(",".join([key, *formatted_tags]), value)
