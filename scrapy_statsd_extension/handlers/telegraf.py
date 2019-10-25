from telegraf.client import TelegrafClient

from scrapy_statsd_extension import utils, defaults, handlers

class TelegrafHandler(handlers.StatsdBaseHandler):

    def create_client(self, host, port, prefix):
        return TelegrafClient(host, port, prefix)

    def increment(self, key, value, spider):
        if self.not_ignored_field(key) and self.has_valid_prefix(key):
            self.client.metric(key, value) #TODO: add tag support
