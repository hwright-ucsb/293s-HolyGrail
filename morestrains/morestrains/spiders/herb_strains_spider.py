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
        if kind.lower() == ('indica' or 'sativa' or 'hybrids'):

            desc = response.xpath('normalize-space(//div[@class="et_monarch article-body"])').extract()
            desc = str(desc)[3:-2]

            per = response.xpath('//div[@class="strain-data-table-data-row"]//span[@class="strain-item"]/text()').extract()
            percents = {}
            if len(percents) > 0:
                percents['thc'] = str(per[0].split("%")[0])
                percents['cbd'] = str(per[0].split("%")[1])

            l_links = response.xpath('//div[@class="strain-lineage"]/a/text()').extract()
            l_strings = response.xpath('//div[@class="strain-lineage"]/text()').extract() 
            lineage = []
            if (len(l_links) + len(l_strings)) > 0:
                for s in l_links:
                    lineage.append(str(s))
                for s in l_strings:
                    lineage.append(str(s))

            attr_names1 = response.xpath('//div[@class="recipe-detail-method"]//h3/text()').extract()
            attr_info1 = response.xpath('//div[@class="recipe-detail-method"]//div').extract() 
            attr_names2 = response.xpath('//div[@class="recipe-detail-ingredients"]//h3/text()').extract()
           # attr_info2 = 



            yield {
                'strain': strain_name,
                'kind': kind,
                'description': desc,
                'effects': effects,
                'helps': helps,
                'negative-effects': neffects,
            }
            





