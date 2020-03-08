from os import environ

from datadog import ThreadStats, initialize, statsd

from scrapy_statsd_extension import handlers, defaults


class DatadogHandler(handlers.StatsdBaseHandler):
    def __init__(self, crawler_settings):
        super().__init__(crawler_settings)

        api_key = crawler_settings.get(
            "DATADOG_API_KEY", environ.get("DATADOG_API_KEY")
        )
        namespace = crawler_settings.get("STATSD_PREFIX", defaults.STATSD_PREFIX)

        initialize(api_key=api_key, statsd_namespace=namespace)

    def create_client(self, host, port, prefix):
        return statsd

    def get_tags(self, spider):
        tags = super().get_tags(spider)
        return [f"{key}:{value}" for key, value in tags.items()]

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.increment(key, value, tags=self.get_tags(spider))
