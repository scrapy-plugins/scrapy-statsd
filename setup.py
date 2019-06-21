from setuptools import setup, find_packages


setup(
    name='scrapy-statsd-extension',
    version='0.1.0',
    url='https://github.com/scrapy-plugins/scrapy-statsd',
    description='Scrapy extenstion to log stats to statsd',
    author='Scrapy developers',
    license='BSD',
    packages=find_packages(exclude=('tests', 'tests.*')),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Twisted>=16.0.0',
        'Scrapy>=1.6.0',
        'statsd>=3.3.0'
    ],
)
