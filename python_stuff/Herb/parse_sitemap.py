f = open('herbsitemap.txt','r')
g = open('herb_strains.xml','w')

g.write('<urlset xmlns:image="http://www.google.com/schemas/sitemap-images/1.1" xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')

# only one line
#links = []
for line in f:
	stuff = line.split(' ')
	for thing in stuff:
		if thing.startswith('http://herb.co/strains'):
			g.write('\n\t<url>\n')
			g.write('\t\t<loc>')
			g.write(thing)
			g.write('</loc>\n')
			g.write('\t</url>')
			#links.append(thing)

g.write('\n</urlset>')
f.close()
g.close()