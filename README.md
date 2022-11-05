# scrapy-statsd-extension

The scrapy-statsd-extension is a scrapy extension to send scrapy stats
to statsd host.

## Naming

Scrapy stats names will be mapped to names supported by statsd. Some
examples:

    downloader/request_bytes -> downloader.request_bytes
    downloader/request_method_count/GET -> downloader.request_method_count.GET
    finish_reason -> finish_reason
    robotstxt/exception_count/<class 'PermissionError'> -> robotstxt.exception_count.class_PermissionError

## Installation

Install scrapy-statsd-extension using `pip`:

    pip install scrapy-statsd-extension

## Configuration

First, you need to include the extension to your `EXTENSIONS` dict in
`settings.py`, like so:

    STATSD_ENABLED = True

    EXTENSIONS = {
        ...
        'scrapy_statsd.StatsdExtension': 123,
        ...
    }

## Settings

To configure host settings, you can adjust the following:

    STATSD_HOST = 'localhost'
    STATSD_PORT = 8125

The default endpoint for sending stats will be:

    http://localhost:8125

To enable the extension you must set:

    STATSD_ENABLED = False

Periodic logging is enabled by default but you can disable it, in which
case the metrics will be logged only once, when a spider is closed:

    STATSD_LOG_PERIODIC = True

By default, stats are logged every 5 seconds, you can adjust that using
`STATSD_LOG_EVERY` which is the number of seconds between logging
operations:

    STATSD_LOG_EVERY = 5

Set the desired prefix:

    STATSD_PREFIX = 'scrapy'

You can specify which prefixes you want logged if you don't want all
scrapy stats. The default is an empty list which indicates that all
stats should be logged. You can, for example, log only downloader and
robotstxt exception stats by setting `STATSD_LOG_ONLY` to
`['downloader', 'robotstxt.exception_count']`.

    STATSD_LOG_ONLY = []

You can also specify prefixes to ignore the same way using
`STATSD_IGNORE`:

    STATSD_IGNORE = []

## Tags

Certain platforms such as datadog and influxdb offer tagging options.

To enable tagging set `STATSD_TAGGING` to `True`, it is disabled by
default:

    STATSD_TAGGING = False

Then, you can set custom tags using `STATSD_TAGS`. Currently, only
`spider_name_tag` is supported and setting it to True will add the
spider's as a tag on all metrics:

    STATSD_TAGS = {
        'spider_name_tag': True
    }

You can also set custom tags by setting `statsd_tags` attribute on each
spider. This must be a dictionary containing tag names as keys and tag
values as dictionary values.
