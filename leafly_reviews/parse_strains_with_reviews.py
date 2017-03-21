import json, re

def removeUnicode(s):
	#a mismatch of unicode in hex and usyntax
	noUni = s.encode('utf-8')\
	.replace("\\x92", "'")\
	.replace("\\", '')\
	.replace("\xe2\x80\x99", "'")\
	.replace("\xc2\xa0", ' ')\
	.replace("x93", '"')\
	.replace("x94", '"')\
	.replace("u2019", "'")\
	.replace("u201c", '"')\
	.replace("u201d", '"')\
	.replace("u2028", "\n")

	#for things like that's or she'll
	noUni = re.sub(r'([^ ])\?([^ ])', r"\1'\2", noUni)

	#for things in quotes like ?Oriental Thai blah..?
	noUni = re.sub(r'[ ]\?(.*?)\?[ ]', r' "\1" ', noUni)

	#I'm too lazy to figure out which desc thats from but
	#I'll assume its supposed to be a ' char
	noUni = re.sub('Sage N? Sour OG', "Sage N' Sour OG", noUni)

	noUni = noUni.replace("<", "").replace(">", "").replace("&", "and")

	return noUni



def writeToFile(raw_data):
	global cnt, revcnt
	#for strain_name, reviews in raw_data.iteritems():
	for strain_name, content in raw_data.iteritems():
		cnt = cnt + 1
		outfile.write('<doc>\n')
		outfile.write('\t<field name="STRAIN">')
		outfile.write(strain_name)
		outfile.write('</field>\n')
		reviews = content['reviews']
		rev_str = " "
		for rev in reviews:
			rev_str = rev_str + removeUnicode(rev["description"]) + " "
			revcnt = revcnt + 1
		outfile.write('\t<field name="REVIEWS">')
		outfile.write(rev_str)
		outfile.write('</field>\n')
		outfile.write('\t<field name="BODY">')
		outfile.write(content['info'][0]['description'])
		outfile.write('</field>\n')
		kind = content['info'][0]["kind"]
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
		for attr in content['info'][0]['attributes']:
			temp = temp +" "+ str(attr)
		outfile.write(temp)
		outfile.write('</field>\n')
		outfile.write('</doc>\n')




raw_data = {}
cnt = 0
revcnt = 0
outfile = open("reviews_solr-fixed-FINAL.xml", "w")
outfile.write('<add>\n')
infile = json.load(open("strains_reviews-2.json"))
writeToFile(infile)


outfile.write('</add>')
outfile.close()
print("wrote "+ str(cnt)+" strains and "+ str(revcnt)+" reviews")