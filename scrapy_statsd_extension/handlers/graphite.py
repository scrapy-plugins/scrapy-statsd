import graphyte

from scrapy_statsd_extension.handlers import StatsdBaseHandler


class GraphiteHandler(StatsdBaseHandler):
    def create_client(self, host, port, prefix):
        import pudb

        pu.db
        graphyte.init(host, port=port, prefix=prefix)
        return graphyte

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            import pudb

            pu.db

            self.client.send(key, value, tags=self.get_tags(spider))
