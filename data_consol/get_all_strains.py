import json

strains = json.load(open('consol_strains-5.json'))

g = open("unique_strains.txt","w")
for strain_name in strains:
	g.write(strain_name+"\n")
g.close()