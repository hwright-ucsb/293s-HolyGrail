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


    def add_err_url(self, strain_id):
        g = open('bad_ids.txt','a')
        g.write(str(strain_id))
        g.write('\n')
        g.close()


    def parse(self, response):
        strain_id = response.url.split("/")[-1]
        if response.status == 404:
            error_urls.append(strain_id)
            add_err_url(strain_id)
        else:
            strain = response.xpath('normalize-space(//div[@id="details_product_name"])').extract()
            strain = str(strain)[3:-2]
            
            sat_ind_ratio = response.xpath('normalize-space(//div[@id="details_product_sativa_indica"])').extract()
            sat_ind_ratio = str(sat_ind_ratio)[3:-2]

            # hasMed = response.xpath('normalize-space(//div[@id="details_overview"])').extract()
            # hasMed = str(hasMed)[3:-2]

            medical_uses = "N/A"
            lineage = "N/A"

            for i in range(1,7):
                try:
                    xp = 'normalize-space(//div[@id="info_wrap"]/div[' + str(i) + '])'
                    div = response.xpath(xp).extract()
                    div = str(div)[3:-2]
                    if div.startswith('Medicinal') or div.startswith('medicinal'):
                        xp2 = 'normalize-space(//div[@id="info_wrap"]/div[' + str(i+1) + '])'
                        medical_uses = response.xpath(xp2).extract()
                        medical_uses = str(medical_uses)[3:-2]
                    if div.startswith('Line') or div.startswith('line'):
                        xp2 = 'normalize-space(//div[@id="info_wrap"]/div[' + str(i+1) + '])'
                        lineage = response.xpath(xp2).extract()
                        lineage = str(lineage)[3:-2]
                except:
                    pass

            # if hasMed.startswith('Medicinal') or hasMed.startswith('medicinal'):
            #     medical_uses = response.xpath('normalize-space(//div[@id="details_lineage"])').extract()
            #     medical_uses = str(medical_uses)[3:-2]

            # hasLineage = response.xpath('normalize-space(//div[@id="info_wrap"]/div[7])').extract()

            additional_info = response.xpath('normalize-space(//div[@id="reviews_wrap"]/p)').extract()
            additional_info = str(additional_info)[3:-2]

            yield {
                'strain': strain,
                'sat_ind_ratio': sat_ind_ratio,
                'medical_uses': medical_uses,
                'lineage': lineage,
                'description': additional_info,
            }

        

    



