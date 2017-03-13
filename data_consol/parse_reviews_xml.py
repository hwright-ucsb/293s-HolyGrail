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
	global cnt
	#for strain_name, reviews in raw_data.iteritems():
	reviews=raw_data
	for i in range(0, len(reviews)):
		strain_name = reviews[i]["strain"]
		strain_name = strain_name.replace("-"," ")
		if strain_name in strains:
			cnt = cnt+1
			outfile.write('<doc>\n')
			outfile.write('\t<field name="REVIEWID">')
			outfile.write(reviews[i]['ID'])
			outfile.write('</field>\n')
			outfile.write('\t<field name="STRAIN">')
			outfile.write(strain_name)
			outfile.write('</field>\n')
			outfile.write('\t<field name="SOURCE">')
			outfile.write("LEAFLY")
			outfile.write('</field>\n')
			outfile.write('\t<field name="BODY">')
			outfile.write(removeUnicode(reviews[i]['content']))
			outfile.write('</field>\n')
			outfile.write('\t<field name="STARS">')
			outfile.write(reviews[i]['stars'])
			outfile.write('</field>\n')
			outfile.write('\t<field name="DATE">')
			outfile.write(str(reviews[i]['date']))
			outfile.write('</field>\n')
			outfile.write('\t<field name="USER">')
			outfile.write(removeUnicode(reviews[i]['user']))
			outfile.write('</field>\n')
			outfile.write('\t<field name="attributes">')
			temp = ""
			for attr in reviews[i]['attributes']:
				temp = temp +" "+ str(attr)
			outfile.write(temp)
			outfile.write('</field>\n')
			outfile.write('</doc>\n')


raw_data = {}
cnt = 0
strains = set()
outfile = open("reviews_solr-fixed.xml", "w")

strainfile = "unique_strains.txt"
f = open(strainfile,"r")
for strain in f:
	strains.add(strain.strip())
outfile.write('<add>\n')

s = "json/leafly-reviews-"
for i in range(0, 14):
	t = s + str(i+1) + ".json"
	writeToFile(json.load(open(t)))
	print("wrote " + t)






outfile.write('</add>')
outfile.close()
print("wrote "+ str(cnt)+" reviews")
