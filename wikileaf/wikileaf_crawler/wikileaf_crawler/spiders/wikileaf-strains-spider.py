import scrapy
import urllib2
import xml.etree.ElementTree
import time


class WikileafStrainsSpider(scrapy.Spider):
    name = "wikileaf-strains"

    def start_requests(self):

        fname = urllib2.urlopen('https://www.wikileaf.com/sitemap/')
        root = xml.etree.ElementTree.parse(fname).getroot()

        urls = []
        for child in root:
            temp = child[0].text.split("/")
            if len(temp)==6 and temp[3]=='strain':
                urls.append(child[0].text)
        
        print(len(urls))
        i = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            i = i + 1
            #if i == 10:
            #    break


    def parse(self, response):

        strain_name = response.url.split("/")[-2]
        kind = response.xpath('//div[@class="breadcumb"]').extract()[0].split("/")[-6]
        description = response.xpath('normalize-space(//div[@itemprop="description"])').extract()
        usage_time = response.xpath('//div[@class="strain-time-icon"]//@alt').extract()[0]
        parents = response.xpath('//div[@class="strain-side-box parent"]//li/a/text()').extract()
        thc_content = {
            'high_THC': response.xpath('//div[@class="graph-val"]/text()').extract()[1],
            'avg_THC': response.xpath('//div[@class="graph-val"]/text()').extract()[2],
            'kind': response.xpath('normalize-space(//div[@class="strain-type-text"]/text())').extract()[0],
        }
        attributes = {}

        stars = response.xpath('//span[@class="disp-rating"]/text()').extract()
        if len(stars) > 0:
            stars = str(stars[0])
        else:
            stars = '-1'

        countries = response.xpath('//div[@class="strain-side-box country"]//li/text()').extract()
        bars = response.xpath('//div[@class="strain-bar"]/input/@id').extract()

        for i in range(0,len(bars)-3):
            attributes[str(response.xpath('//div[@class="strain-bar"]/input/@id').extract()[i+3])] = str(response.xpath('//div[@class="strain-bar"]/input/@value').extract()[i+3])


        yield {
            'strain': strain_name,
            'parent_strains': parents,
            'lineage': countries,
            'kind': kind,
            'stars': stars,
            'description': description,
            'time_of_day': usage_time,
            'percents': thc_content,
            'attributes': attributes,

        }

        #page = response.url.split("/")[-1]
        #filename = 'strain-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)



