from enum import Enum
import json


class Source(Enum):
	HERB = 1
	LEAFLY = 2
	WIKILEAF = 3
	FOURTWENTY101 = 4
	QANNABIS = 5
	CANNABISREPORTS = 6


strains = {}

#def importHerb(file):



#def importLeafly(file):



#def importWikileaf(file):


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
		

		# if len(kind_s[0]) > 0 and (kind_s[1]) > 0:
		# 	kind = populateKind(int(kind_s[1]), int(kind_s[0]), 0) #indica first then sativa
		# elif len(kind_s[0]) > 0 and (kind_s[1]) == 0:
		# 	kind = populateKind(0, int(kind_s[0]), 0) 
		# elif len(kind_s[0]) == 0 and (kind_s[1]) > 0:
		# 	kind = populateKind(int(kind_s[1]), 0, 0) 
		# else:
		# 	kind = populateKind(0,0,-1)

		medical_uses = cur["medical_uses"].lower()
		medical_uses = medical_uses.split(", ")
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


def addToStrain(strain_name, source, kind, attributes, descr):
	strains[strain_name].append({"source": source.name, 
									"kind": kind, 
									"attributes": attributes, 
									"description": descr})
	#print(strains[strain_name])

def populateKindManual(kind):
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

def populateKind(indica, sativa, flag):
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

def main():
	importFourTwenty101('strains420101.json')
	importQannabis('qannabis_strains.json')

	for k in strains.keys():
		print(k +" " + str(len(strains[k])))

	json.dump(strains, open('consol_strains.json', 'w'))
main()

