import scrapy
import urllib2
import xml.etree.ElementTree
import time


class StrainsSpider(scrapy.Spider):
    name = "strains"

    def start_requests(self):

        fname = urllib2.urlopen('https://www.leafly.com/sitemap/strains')
        root = xml.etree.ElementTree.parse(fname).getroot()

        urls = []
        for child in root:
            temp = child[0].text.split("/")
            if (temp[3]=='hybrid' or temp[3]=='indica' or temp[3]=='sativa') and len(temp)==5:
                urls.append(child[0].text)
        
        print(len(urls))
        i = 0
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            i = i + 1


    def parse(self, response):

        strain_name = response.url.split("/")[-1]
        kind = response.url.split("/")[-2]
        
        yield {
            'strain': strain_name,
            'kind': kind,
            'description': response.xpath('normalize-space(//div[@itemprop="description"]//p)').extract(),
        }

        #page = response.url.split("/")[-1]
        #filename = 'strain-%s.html' % page
        #with open(filename, 'wb') as f:
        #    f.write(response.body)
        #self.log('Saved file %s' % filename)



