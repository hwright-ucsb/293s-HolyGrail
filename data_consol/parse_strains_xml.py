import json


raw_data = {}

outfile = open("strains_solr.xml", "w")

# s = "leafly-strains-"
# for i in range(0, 14):
# 	t = s + str(i+1) + ".json"
# 	raw_data.extend(json.load(open(t)))


cnt = 1
raw_data = json.load(open('consol_strains-5.json'))
outfile.write('<add>\n')

for strain_name, entries in raw_data.iteritems():
	for i in range(0, len(entries)):
		outfile.write('<doc>\n')
		outfile.write('\t<field name="DOCNO">')
		outfile.write(str(cnt))
		cnt = cnt + 1
		outfile.write('</field>\n')
		outfile.write('\t<field name="STRAIN">')
		outfile.write(strain_name)
		outfile.write('</field>\n')
		outfile.write('\t<field name="SOURCE">')
		outfile.write(entries[i]['source'])
		outfile.write('</field>\n')
		outfile.write('\t<field name="BODY">')
		outfile.write(entries[i]['description'])
		outfile.write('</field>\n')
		kind = entries[i]["kind"]
		outfile.write('\t<field name="KIND_INDICA">')
		outfile.write(str(kind[0]))
		outfile.write('</field>\n')
		outfile.write('\t<field name="KIND_SATIVA">')
		outfile.write(str(kind[1]))
		outfile.write('</field>\n')
		outfile.write('\t<field name="KIND_SETMANUALLY">')
		outfile.write(str(kind[2]))
		outfile.write('</field>\n')
		outfile.write('\t<field name="attributes">')
		temp = ""
		for attr in entries[i]['attributes']:
			temp = temp +" "+ str(attr)
		outfile.write(temp)
		outfile.write('</field>\n')
		outfile.write('</doc>\n')

outfile.write('</add>')
outfile.close()
