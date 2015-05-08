# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.utils.python import unicode_to_str

from fcntl import ioctl

import os

import struct

RNDADDENTROPY = 1074287107

class TruenetSpider(CrawlSpider):
    name = "truenet"
    allowed_domains = ["truenet.co.nz"]
    start_urls = (
        'https://www.truenet.co.nz/news/all',
    )

    rules = (
      (Rule(LinkExtractor(allow=(".*/articles/.*")), callback = 'parse_article'),)
    )

    def parse_article(self, response):
      content = unicode_to_str(response.body_as_unicode(),'latin-1','ignore')
      for block in [content[i:i+1000] for i in range(0, len(content), 1000)]:
        # Build the datastructure that RNGADDENTROPY requires
        format = 'ii%is' % len(block)
        entropy_data = struct.pack(format, 8 * len(block), len(block), block)
        # Call the RNGADDENTROPY ioctl
        random_dev_fd = os.open('/dev/random', os.O_WRONLY)
        ioctl(random_dev_fd, RNDADDENTROPY, entropy_data)
        os.close(random_dev_fd)
