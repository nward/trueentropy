from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from trueentropy.spiders.truenet import TruenetSpider
from scrapy.utils.project import get_project_settings

def get_more_entropy():
  spider = TruenetSpider(domain='truenet.co.nz')
  settings = get_project_settings()
  crawler = Crawler(settings)
  crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
  crawler.configure()
  crawler.crawl(spider)
  crawler.start()
  log.start()
  reactor.run()

get_more_entropy()