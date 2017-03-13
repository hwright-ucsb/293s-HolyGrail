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

	# get percentage of each attribute				
	attributes = {}
	for src in attr_in_review:
		if src not in attr_from_src:
			# DISCREPANCY deal with this later
			pass
		attributes[src] = attr_in_review[src]/float(num_reviews)

	# convert list of values into their avg
	for a in attr_value:
		attr_value[a] = sum(attr_value[a])/float(len(attr_value[a]))

	# there are attributes from info that arent in review
	for src in attr_from_src:
		if src not in attr_in_review:
			# DISCREPANCY
			pass

	# add attributes from info to final attribute dictionary
	for a in attr_value:
		if a in attributes:
			# both info and review had this attr - compare them later????
			attributes[a] = (attributes[a] + attr_value[a]) / 2.0 # just do avg
		else:
			# info had this attr but review didnt
			attributes[a] = attr_value[a]

	strain_rating[strain] = {'avg': avg_star,
							 'attributes': attributes}




data = json.load(open('strains_reviews-2.json'))
# print len(data)
for strain_name in data:
	obj = data[strain_name]

	info = obj['info']
	rev = obj['reviews']

	attr_from_src = {}
	for i in info:
		if i['source'] == 'LEAFLY' or i['source'] == 'WIKILEAF':
			attr_from_src[i['source']] = i['attributes']

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

	# print attr_from_src
	for src in attr_from_src:
		for a in attr_from_src[src]:
			# print attr_from_src[src][a]
			attr_from_src[src][a] = float(attr_from_src[src][a]) / float(100)

	# print attr_from_src
	num_reviews = len(rev)

	calcRating(strain_name, star_ratings, attr_from_src, attr_in_review, num_reviews)

print strain_rating