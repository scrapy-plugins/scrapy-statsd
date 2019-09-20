from os import environ

from datadog import ThreadStats, initialize, statsd

from scrapy_statsd_extension import handlers


class DatadogHandler(handlers.StatsdBaseHandler):
    def __init__(self, crawler_settings):
        super().__init__(crawler_settings)

        api_key = crawler_settings.get(
            "STATSD_DDOG_API_KEY", environ.get("DATADOG_API_KEY")
        )
        app_key = crawler_settings.get(
            "STATSD_DDOG_APP_KEY", environ.get("DATADOG_APP_KEY")
        )

        initialize(api_key=api_key, app_key=app_key)

    def create_client(self, host, port, prefix):
        stats_client = ThreadStats()
        stats_client.start()
        return stats_client

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.gauge(key, value, tags=self.get_tags(spider))
