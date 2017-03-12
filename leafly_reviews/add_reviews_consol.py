import json, re

strains = {} # final result here
reviews = {} # keep in memory review info

# store reviews in dictionary to find review for specific strain faster
def addReview(file):
	data = json.load(open(file))
	for i in range(len(data)):
		cur = data[i]
		strain_name = cur["strain"]
		strain_name = strain_name.replace("-"," ")
		reviews[strain_name] = cur

addReview("json/leafly-reviews-1.json")
addReview("json/leafly-reviews-2.json")
addReview("json/leafly-reviews-3.json")
addReview("json/leafly-reviews-4.json")
addReview("json/leafly-reviews-5.json")
addReview("json/leafly-reviews-6.json")
addReview("json/leafly-reviews-7.json")
addReview("json/leafly-reviews-8.json")
addReview("json/leafly-reviews-9.json")
addReview("json/leafly-reviews-10.json")
addReview("json/leafly-reviews-11.json")
addReview("json/leafly-reviews-12.json")
addReview("json/leafly-reviews-13.json")
addReview("json/leafly-reviews-14.json")

strain_json = json.load(open('consol_strains-5.json'))
for strain_name, entry in strain_json.iteritems():
	if strain_name in reviews:
		entry.append({"leafly-review":reviews[strain_name]})
	else:
		entry.append({"leafly-review":"N/A"})
	strains[strain_name] = entry

json.dump(strains, open('strains_reviews.json', 'w'))