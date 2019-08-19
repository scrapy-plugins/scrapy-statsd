# scrapy-statsd-extension
The scrapy-statsd-extension is a scrapy extension to send scrapy stats to statsd host.


## Installation
Install scrapy-statsd-extension using ``pip``:

    $ pip install scrapy-statsd-extension


## Configuration
First, you need to include the extension to your ``EXTENSIONS`` dict in
``settings.py``, like so:

    STATSD_ENABLED = True

    EXTENSIONS = {
        ...
        'scrapy_statsd_extension.StatsdExtension': 123,
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

Periodic logging is enabled by default but you can disable it, in which case
the metrics will be logged only once, when a spider is closed:

    STATSD_LOG_PERIODIC = True

By default, stats are logged every 5 seconds, you can adjust that using
``STATSD_LOG_EVERY`` which is the number of seconds between logging operations:

    STATSD_LOG_EVERY = 5
