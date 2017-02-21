import scrapy
import urllib2
import xml.etree.ElementTree
import time


class WikileafStrainsSpider(scrapy.Spider):
    name = "qannabis-strains"
    error_urls = []

    def start_requests(self):

        base_url = 'http://marqaha.herokuapp.com/gallery/flowers/'

        urls = []
        for i in range(1,10000):
            url = base_url + str(i)
            urls.append(url)

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        review_id = response.url.split("/")[-1]
        if response.status == 404:
            error_urls.append(review_id)
        else:
            strain = response.xpath('normalize-space(//div[@id="details_product_name"])').extract()
            strain = str(strain)[3:-2]
            
            sat_ind_ratio = response.xpath('normalize-space(//div[@id="details_product_sativa_indica"])').extract()
            sat_ind_ratio = str(sat_ind_ratio)[3:-2]

            medical_uses = response.xpath('normalize-space(//div[@id="details_lineage"])').extract()
            medical_uses = str(medical_uses)[3:-2]

            additional_info = response.xpath('normalize-space(//div[@id="reviews_wrap"]/p)').extract()
            additional_info = str(additional_info)[3:-2]

            yield {
                'strain': strain,
                'sat_ind_ratio': sat_ind_ratio,
                'medical_uses': medical_uses,
                'description': additional_info,
            }



