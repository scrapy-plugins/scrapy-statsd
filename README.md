
# scrapy-statsd-extension
The scrapy-statsd-extension is a scrapy extension to send scrapy stats to statsd host.


## Installation
Install scrapy-jsonrpc using ``pip``::

    $ pip install scrapy-statsd-extension


## Configuration
First, you need to include the entension to your ``EXTENSIONS`` dict in
``settings.py``, like so:

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
