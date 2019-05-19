import statsd
import time

client = statsd.StatsClient('localhost', 8125)

for i in range(10):
    time.sleep(1)
    client.incr('foo')
