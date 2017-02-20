import scrapy
from scrapy.selector import HtmlXPathSelector
from scrapy.spider import BaseSpider
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
import xml.etree.ElementTree

# this spider gets strains from herb.co

domain = 'herb.co'
strains = 'http://herb.co/strains'
ind_strains = 'http://herb.co/straincategory/indica/'
sat_strains = 'http://herb.co/straincategory/sativa/'
hyb_strains = 'http://herb.co/straincategory/hybrid/'

class Strains1Spider(scrapy.Spider):
    name = "herb_strains"

    def start_requests(self):
        # this xml contains all strains
        root = xml.etree.ElementTree.parse('herb_strains.xml').getroot()
        urls = []

        for child in root:
            urls.append(child[0].text)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        
        strain_name = ""
        kind = ""
        desc = ""

        yield {
            'strain': strain_name
            'kind': kind
            'description': desc
        }
        





