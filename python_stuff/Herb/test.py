import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import xml.etree.ElementTree
from lxml import html
from pprint import pprint

# To run:
# scrapy runspider test.py > output.txt

# check contents of output.txt to see if you have well formed info


class TestSpider(scrapy.Spider):
    name = 'strains'

    test1 = 'http://www.leafly.com/hybrid/100-og'
    test2 = 'http://herb.co/strains/afghan-kush/'
    
    start_urls = [test2]


    def parse(self, response):
        r = response.url.split('/')
        #pprint (vars(response))
        #tree = html.fromstring(response.content)
        kind = response.xpath('normalize-space(//div[@id="submenu-current-page"])').extract()
        kind = str(kind)[3:-2]
        desc = response.xpath('normalize-space(//div[@class="et_monarch article-body"])').extract()
        desc = str(desc)[3:-2]
        print "strain: ", r[-2]
        print "kind: ", kind
        print "desc: ", desc






