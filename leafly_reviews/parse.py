# script to make txt file for lucene indexing (WIP)
import json

outfile = 'all_data.txt'
g = open(outfile,'w')

# format
# strain_name:src:kind:attributes:desc:review
data = json.load(open('strains-reviews-1.json'))
for i in range(len(data)):
	cur = data[i]

