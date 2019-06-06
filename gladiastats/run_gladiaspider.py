from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings
from spiders.gladiaspider import GladiaspiderSpider

import sys

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
settings = get_project_settings()
settings.set('FEED_FORMAT', 'csv')
settings.set('FEED_URI', 'stats.csv')

runner = CrawlerRunner(settings)
if len(sys.argv) > 1:
    d = runner.crawl(GladiaspiderSpider, max_r=sys.argv[1])
else:
    d = runner.crawl(GladiaspiderSpider, max_r='100')
d.addBoth(lambda _: reactor.stop())
reactor.run() # the script will block here until the crawling is finished