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
            'high': response.xpath('//div[@class="graph-val"]/text()').extract()[1],
            'avg': response.xpath('//div[@class="graph-val"]/text()').extract()[2],
            'kind_percent': response.xpath('normalize-space(//div[@class="strain-type-text"]/text())').extract()[0],
        }
        medical_uses = {}
        effects = {}

        for i in range(0,5):
            medical_uses[str(response.xpath('//div[@class="strain-bar"]/input/@id').extract()[i+3])] = str(response.xpath('//div[@class="strain-bar"]/input/@value').extract()[i+3])
            effects[str(response.xpath('//div[@class="strain-bar"]/input/@id').extract()[i+8])] = str(response.xpath('//div[@class="strain-bar"]/input/@value').extract()[i+8])

        yield {
            'strain': strain_name,
            'parent_strains': parents,
            'kind': kind,
            'description': description,
            'time_of_day': usage_time,
            'thc_content': thc_content,
            'medical_uses': medical_uses,
            'effects': effects,

        }

        #page = response.url.split("/")[-1]
        #filename = 'strain-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)



