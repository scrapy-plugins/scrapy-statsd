from scrapy_statsd_extension.utils import create_stat_key


def test_create_stat_key():
    assert create_stat_key("dummy-key") == "dummy-key"