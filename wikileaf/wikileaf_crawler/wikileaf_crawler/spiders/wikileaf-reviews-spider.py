import scrapy
import urllib2
import xml.etree.ElementTree
import time


class WikileafReviewsSpider(scrapy.Spider):
    name = "wikileaf-reviews"

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
        stars = response.xpath('//div[@class="review-stars"]/i[@class="material-icons"]/text()').extract()
        num_reviews = (len(stars)/5) - 1    #if there are reviews, 1st 5 stars are always the 'overall' rating
        
        reviews = []
        if num_reviews > 0:
            for i in range(0,num_reviews):
                tmp = 0
                for j in range(0,5):
                    if stars[5+(i*5)+j] == 'star':
                        tmp = tmp + 1
                    elif stars[5+(i*5)+j] == 'star_half':
                        tmp = tmp + 0.5

                reviews.append({
                    'stars': tmp,
                    'content': response.xpath('normalize-space(//div[@class="review-item-content"]['+str(i+1)+']/text())').extract(),
                    }) 

        yield {
            'strain': strain_name,
            'reviews_list': reviews,

        }


