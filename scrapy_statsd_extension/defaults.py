STATSD_ENABLED = False
STATSD_HOST = "localhost"
STATSD_PORT = 8125
STATSD_LOG_PERIODIC = True
STATSD_LOG_EVERY = 5
<<<<<<< Updated upstream
STATSD_HANDLER = "scrapy_statsd_extension.handlers.StatsdBase"
STATSD_PREFIX = "scrapy"
=======
STATSD_HANDLER = 'scrapy_statsd_extension.handlers.graphite.GraphiteHandler'
STATSD_PREFIX = 'scrapy'
>>>>>>> Stashed changes
STATSD_LOG_ONLY = []
STATSD_IGNORE = []
STATSD_TAGGING = False
STATSD_TAGS = {"spider_name": True}
