import json, re

strain_rating = {}

def calcRating(strain, star_ratings, attr):
	if star_ratings:
		avg_star = sum(star_ratings)/float(len(star_ratings))
		strain_rating[strain] = {'avg': avg_star}
	else:
		strain_rating[strain] = {'avg': '-1'}





data = json.load(open('strains_reviews-2.json'))
# print len(data)
for strain_name in data:
	obj = data[strain_name]

	info = obj['info']
	rev = obj['reviews']

	attr_from_src = {} # unused for now
	attr = {}
	for i in info:
		if i['source'] == 'LEAFLY': # seems like leafly is the only one to have useful attributes
			attr_from_src[i['source']] = i['attributes'] # unused for now
			attr = i['attributes']

	star_ratings = []
	for r in rev:
		star = float(r['stars'])
		star_ratings.append(star)

	calcRating(strain_name, star_ratings, attr)

print strain_rating