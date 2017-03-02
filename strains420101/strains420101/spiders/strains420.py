import scrapy
import urllib2
import xml.etree.ElementTree
import time


class Strains420101Spider(scrapy.Spider):
    name = "strains-420101"

    def start_requests(self):

        urls = []
        f = open('strains420urls.txt','r')
        for line in f:
            urls.append(str(line)[:-1])
        f.close()

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        # shit = 'https://420101.com/strains/view/lavender'
        # yield scrapy.Request(url=shit, callback=self.parse)


    def parse(self, response):
        strain = response.xpath('normalize-space(//div[@id="strain-meta-left"]//h2)').extract()
        strain = str(strain)[3:-2]

        kind = response.xpath('normalize-space(//div[@class="col-md-12"]//h2)').extract()
        kind = str(kind)[3:-2]

        medical_uses = response.xpath('normalize-space(//div[@id="amenity-list"]//ul)').extract()
        medical_uses = str(medical_uses)[3:-2]

        desc = response.xpath('normalize-space(//div[@id="club-about"])').extract()
        desc = str(desc)[3:-2]

        yield {
            'strain': strain,
            'kind': kind,
            'medical_uses': medical_uses,
            'description': desc,
        }



