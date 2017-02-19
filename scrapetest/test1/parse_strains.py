import xml.etree.ElementTree

e = xml.etree.ElementTree.parse('strains.xml').getroot()

print(e[0][0].text)
print(e[4][0].text)