## Plan: 
#			-leafly has reviews with reviewID's; if you enter a URL
#				with a spec. reviewID, no matter what the rest of the URL
#				is it will redirect to review
#			-simply crawl raw ID urls and let it redirect us to correct page
#			-when we get to the redirected page, get the correct associated strain
#				from the response URL 

# Review components:
#			
#			- <span star-rating="x"
#			- review body/content
#			- 3 headings / and attribute lists: form & method, effects, flavor profile 
#
#########################################################################################

import scrapy

class ReviewsSpider(scrapy.Spider):
	name = "reviews"
	handle_httpstatus_list = [404]

	def start_requests(self):
		dummy_url = 'https://www.leafly.com/hybrid/1024/reviews/'
		global bad_urls, error_urls
		bad_urls=open("bad_urls.txt", "w")
		error_urls=[]
 #remember *** need to check item 150,000
		i=235000;
		flag = False
		while not flag:
			url = dummy_url + str(i)
			yield scrapy.Request(url=url, callback=self.parse)
			i = i + 1

			if i == 265000:
				flag = True


	def parse(self, response):

		review_id = response.url.split("/")[-1]

		if response.status == 404:
			error_urls.append(review_id)
		else:
			strain_name = response.url.split("/")[4]
			rating = response.xpath('//div[@class="padding-rowItem copy--centered"]/span[@star-rating]').extract()
			rating = rating[0].split('"')[1]
			time_of_review = response.xpath('//time[@datetime]/text()').extract()[0]
			reviewer_name = response.xpath('//div[@class="l-centered copy--xxxl padding-rowItem color--default [ reviewer-info reviewer-name]"]/text()').extract()[0]
			review_text = response.xpath('//div[@class="copy--md copy-md--xl padding-rowItem--xl notranslate"]/text()').extract()
			if len(review_text) > 0:
				review_text = review_text[0]
			else:
				review_text=''
			attributes = response.xpath('//ul[@class="attributes copy--xxs m-pills"]/li/text()').extract()

			yield {
				'strain':		strain_name,
				'ID':			review_id,
				'stars':		rating,
				'date':			time_of_review,
				'user':		reviewer_name,
				'content':		review_text,
				'attributes':	attributes,
			}


	def closed(self, reason):
		for num in error_urls:
			bad_urls.write(str(num)+', ')
		bad_urls.close()

