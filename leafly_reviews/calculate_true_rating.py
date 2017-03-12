import json, re

def calcRating(review):
	pass

data = json.load(open('strains_reviews-2.json'))
print len(data)
for i in range(len(data)):
	cur = data[i]
	rev = cur['reviews']
	print rev['description']