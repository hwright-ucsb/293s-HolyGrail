import scrapy
# from scrapy.selector import HtmlXPathSelector
# from scrapy.spider import BaseSpider
# from scrapy.http import Request
# from scrapy.linkextractors import LinkExtractor
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

        strain_name = response.url.split('/')[-2]
        kind = response.xpath('normalize-space(//div[@id="submenu-current-page"])').extract()
        kind = str(kind)[3:-2]
        desc = response.xpath('normalize-space(//div[@class="et_monarch article-body"])').extract()
        desc = str(desc)[3:-2]

        effects = response.xpath('normalize-space(//div[@class="recipe-detail-ingredients-method-container"]/div[1])').extract()
        effects = str(effects)[12:-2]

        helps = response.xpath('normalize-space(//div[@class="recipe-detail-ingredients-method-container"]/div[16])').extract()
        helps = str(helps)[12:-2]

        neffects = response.xpath('normalize-space(//div[@class="recipe-detail-ingredients-method-container"]/div[19])').extract()
        neffects = str(neffects)[22:-2]

        yield {
            'strain': strain_name,
            'kind': kind,
            'description': desc,
            'effects': effects,
            'helps': helps,
            'negative-effects': neffects,
        }
        





