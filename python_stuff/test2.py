import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import xml.etree.ElementTree
from lxml import html
from pprint import pprint

# To run:
# scrapy runspider test2.py > output.txt

# check contents of output.txt to see if you have well formed info


class TestSpider(scrapy.Spider):
    name = 'strains420'

    base_url = 'https://420101.com/strains/'
    
    urls = []

    for i in range(0,1351,25):
        url = base_url + str(i)
        urls.append(url)

    start_urls = urls


    def parse(self, response):
        hxs = scrapy.Selector(response)
        # extract all links from page
        all_links = hxs.xpath('*//a/@href').extract()
        # iterate over links
        for link in all_links:
            if link.startswith('https://420101.com/strains/view/'):
                print link
 
    