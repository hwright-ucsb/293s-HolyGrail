from enum import Enum
import json
import re

class Source(Enum):
	HERB = 1
	LEAFLY = 2
	WIKILEAF = 3
	FOURTWENTY101 = 4
	QANNABIS = 5
	CANNABISREPORTS = 6


strains = {}

def importHerb(file):
	data = json.load(open(file))

	for i in range(0, len(data)):
		cur = data[i]
		strain_name = splitHyphenatedStrain(cur["strain"])
		kind_s = cur["kind"].lower()
		source = Source.HERB
		if kind_s == "indica":
			kind = populateKindManual(kind_s)
		elif kind_s == "sativa":
			kind = populateKindManual(kind_s)
		elif kind_s == "hybrids":
			kind = populateKindManual("hybrid")
		attributes = {}
		descr = cur["description"]

		if strain_name not in strains:
			initializeStrain(strain_name, source, kind, attributes, descr)
		else:
			addToStrain(strain_name, source, kind, attributes, descr)

		print("Done importing Herb data")


def importLeafly(file):
	data = json.load(open(file))

	for i in range(0, len(data)):
		cur = data[i]
		strain_name=splitHyphenatedStrain(cur["strain"])
		kind = populateKindManual(cur["kind"])
		source = Source.LEAFLY
		attr_raw = cur["attributes"]
		names = []
		values = []
		for name, value in attr_raw.iteritems():
			names.append(name.lower())
			values.append(float(value))

		attributes = setAttributes(names, values)
		descr = cur["description"][0]
		if len(descr) > 1:
			print(strain_name)
			print(descr)

		if strain_name not in strains:
			initializeStrain(strain_name, source, kind, attributes, descr)
		else:
			addToStrain(strain_name, source, kind, attributes, descr)

	print("Done importing Leafly data")


def importWikileaf(file):
	data = json.load(open(file))

	for i in range(0, len(data)):
		cur = data[i]
		strain_name = splitHyphenatedStrain(cur["strain"])
		kind_s = cur["kind"].lower()
		percent_k = int(cur["percents"]["kind"].split("%")[0])
		source = Source.WIKILEAF

		if kind_s == "indica":
			kind = populateKind(percent_k, (100-percent_k), 0)
		elif kind_s == "hybrid":
			kind = populateKind(50, 50, 0)
		elif kind_s == "sativa":
			kind = populateKind((100-percent_k), percent_k, 0)

		attr_raw = cur["attributes"]
		names = []
		values = []
		
		for name, value in attr_raw.iteritems(): #format attributes correctly 
			temp = name.split("avg_")[1].split("_")

			if temp[0] == "cott":
				temp[0] = "cotton"

			temp_s = temp[0]
			for z in range(1, len(temp)):
				temp_s = temp_s + " " + temp[z]
			names.append(temp_s)
			values.append(int(value))

		attributes = setAttributes(names, values)
		descr = cur["description"][0]
		if len(descr) > 1:
			print(descr)
			print(strain_name)
		if strain_name not in strains:
			initializeStrain(strain_name, source, kind, attributes, descr)
		else:
			addToStrain(strain_name, source, kind, attributes, descr)

	print("Done importing Wikileaf data")


def importFourTwenty101(file):
	data = json.load(open(file))


	for i in range(0,len(data)):
		cur = data[i]
		strain_name = cur["strain"].lower()
		kind_s = cur["kind"].lower()
		kind = populateKindManual(kind_s)				## kind percentages not given 
		medical_uses = cur["medical_uses"].lower()
		medical_uses = medical_uses.split(" ")

		attributes = setAttributesManual(medical_uses)
		source = Source.FOURTWENTY101
		descr = cur["description"]

		if strain_name not in strains:
			initializeStrain(strain_name, source, kind, attributes, descr)
		else:
			addToStrain(strain_name, source, kind, attributes, descr)


	print("Done importing 420101 data")


def importQannabis(file):
	data = json.load(open(file))

	for i in range(0, len(data)):
		cur = data[i]
		strain_name = cur["strain"].lower()
		kind_s = cur["sat_ind_ratio"].split(" ")[2].split("/")

		# lineage = cur["lineage"].lower()
		# if len(lineage) == 1:							## wasn't split -- split now
		# 	lineage = lineage[0].split(" x ")

		flag = 0
		try:
			indica = int(kind_s[1])
		except ValueError:
			indica = 0
		try:
			sativa = int(kind_s[0])
		except ValueError:
			sativa = 0
		if sativa == 0 and indica == 0:
			flag = -1
		kind = populateKind(indica, sativa, flag)

		medical_uses = [x.lower() for x in cur["medical_uses"]]
		attributes = setAttributesManual(medical_uses)
		source = Source.QANNABIS
		descr = cur["description"]

		if strain_name not in strains:
			initializeStrain(strain_name, source, kind, attributes, descr)
		else:
			addToStrain(strain_name, source, kind, attributes, descr)

	print("Done importing qannabis data")

#def importCannabisReports(file):

def initializeStrain(strain_name, source, kind, attributes, descr):
	strains[strain_name] = []
	addToStrain(strain_name, source, kind, attributes, descr)

def removeUnicode(descr):
	#a mismatch of unicode in hex and usyntax
	noUni = descr.encode('utf-8')\
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

def addToStrain(strain_name, source, kind, attributes, descr):
	strains[strain_name].append({"source": source.name, 
									"kind": kind,
									"attributes": attributes, 
									"description": removeUnicode(descr)})

def populateKindManual(kind): # automatically sets flag == 1
	s = []
	if kind == 'indica':
		s.append(100)
		s.append(0)
	elif kind == 'sativa':
		s.append(0)
		s.append(100)
	elif kind == 'hybrid':
		s.append(50)
		s.append(50)

	s.append(1)
	return s

def populateKind(indica, sativa, flag): # be sure to set flag == 0
	s = [indica, sativa, flag]
	return s

def setAttributesManual(attr):
	s = {}
	for i in range(0, len(attr)):
		s[attr[i]] = -1

	return s

def setAttributes(attr, values):
	s = {}
	for i in range(0, len(attr)):
		s[attr[i]] = values[i]

	return s

def splitHyphenatedStrain(strain):
	strain_arr = strain.split("-")
	s = strain_arr[0].lower()
	for j in range(1, len(strain_arr)):
			s = s + " " + strain_arr[j].lower()
	return s

def main():
	importFourTwenty101('strains420101.json')
	importQannabis('qannabis_strains_fixed.json')
	importWikileaf('wikileaf_strains_all.json')
	importLeafly('leafly-fixed.json')
	#importHerb('herb_strains.json')

	#for k in strains.keys():
		#if len(strains[k]) > 2:
		#	print(k +" " + str(len(strains[k])))

	json.dump(strains, open('consol_strains-5.json', 'w'))
main()

