from twisted.internet import task


def looping_call_task(callback, *args):
    return task(callback, *args)


def create_stat_key(scrapy_stats_key):
    return scrapy_stats_key
