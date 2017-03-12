import json


raw_data = {}

outfile = ("strains_solr.xml", "w")

s = "leafly-strains-"
for i in range(0, 14):
	t = s + str(i+1) + ".json"
	raw_data.extend(json.load(open(t)))


cnt = 1
	
outfile.write('<add>\n')

for strain_name, entries in raw_data.iteritems():
	for i in range(0, len(entries)):
		outfile.write('<doc>\n')
		outfile.write('\t<field name="DOCNO">')
		outfile.write(str(cnt))
		cnt = cnt + 1
		outfile.write('</field>\n')
		outfile.write('\t<field name="SOURCE">')
		outfile.write(entries[i]['source'])
		outfile.write('</field>\n')
		