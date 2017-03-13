import json, re

strain_rating = {}

def calcRating(strain, star_ratings, attr_from_src, attr_in_review, num_reviews):
	avg_star = -1.0
	if star_ratings:
		avg_star = sum(star_ratings)/float(len(star_ratings))

	# wikileaf and leafly both give numerical ratings to each attr
	# the rest dont
	# 420101 is really inaccurate, so we wont include it

	attr_value = {} # contains numerical values from src, stored as list
	attr_count = {} # contains count of sources that say that strain has that attr


	for src in attr_from_src:
		if src == 'LEAFLY' or src == 'WIKILEAF':
			for a in attr_from_src[src]:
				if a not in attr_value:
					attr_value[a] = []
				attr_value[a].append(attr_from_src[src][a])
				if a not in attr_count:
					attr_count[a] = 1
				else:
					attr_count[a] += 1
		else:
			for a in attr_from_src[src]:
				if a not in attr_value:
					attr_value[a] = []
				attr_value[a].append(-1)
				if a not in attr_count:
					attr_count[a] = 1
				else:
					attr_count[a] += 1

	# NOTE: since some strains have so many reviews,
	# the values in attr_review may be skewed heavily.
	# the values are the percentage of reviews that
	# mention that attribute
	strain_rating[strain] = {'avg': avg_star,
							 'attr_value': attr_value,
							 'attr_count': attr_count,
							 'attr_review': attr_in_review,
							 'num_reviews': num_reviews }






data = json.load(open('strains_reviews-2.json'))
# print len(data)
for strain_name in data:
	obj = data[strain_name]

	info = obj['info']
	rev = obj['reviews']

	attr_from_src = {}
	attr = {}
	for i in info:
		if i['source'] != 'FOURTWENTY101':
			attr_from_src[i['source']] = i['attributes']
			attr = i['attributes']

	star_ratings = []
	attr_in_review = {} # attribute info can be found in both the info AND reviews

	# print strain_name,"has",len(rev),"reviews"

	for r in rev:
		# star stuff
		star = float(r['stars'])
		star_ratings.append(star)

		# attribute stuff
		attrib_list = r['attributes']
		for a in attrib_list:
			if a in attr_in_review:
				attr_in_review[a] += 1
			else:
				attr_in_review[a] = 1

	num_reviews = len(rev)

	calcRating(strain_name, star_ratings, attr_from_src, attr_in_review, num_reviews)

print strain_rating