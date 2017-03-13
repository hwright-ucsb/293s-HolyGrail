import json, re

cnt = 0
notcnt =0
strains = set()
strainfile = "unique_strains.txt"
f = open(strainfile,"r")
for strain in f:
	strains.add(strain.strip())


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

	return noUni


def printNoStrain(file):
	data = json.load(open(file))
	global cnt, notcnt
	for i in range(len(data)):
		cur = data[i]
		strain_name = cur["strain"]
		strain_name = strain_name.replace("-"," ")
		if strain_name not in strains:
			cnt = cnt+1
			#print "FOUND:", strain_name
		else:
			notcnt = notcnt+1
	


printNoStrain("json/leafly-reviews-1.json")
printNoStrain("json/leafly-reviews-2.json")
printNoStrain("json/leafly-reviews-3.json")
printNoStrain("json/leafly-reviews-4.json")
printNoStrain("json/leafly-reviews-5.json")
printNoStrain("json/leafly-reviews-6.json")
printNoStrain("json/leafly-reviews-7.json")
printNoStrain("json/leafly-reviews-8.json")
printNoStrain("json/leafly-reviews-9.json")
printNoStrain("json/leafly-reviews-10.json")
printNoStrain("json/leafly-reviews-11.json")
printNoStrain("json/leafly-reviews-12.json")
printNoStrain("json/leafly-reviews-13.json")
printNoStrain("json/leafly-reviews-14.json")
print(cnt)
print(notcnt)