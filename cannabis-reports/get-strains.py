import time
import json
import urllib2


def add_to_dict(data):
	for j in range(0,10):
		ucpc = str(data[j]['ucpc'])
		all_data[ucpc] = json.dumps(data[j], ensure_ascii=False)


all_data = {}

request = urllib2.Request("https://www.cannabisreports.com/api/v1.0/strains?page=452", #change to start at 452
	headers={"Content-Type" : "application/json", "X-API-Key" : "76935bbe4c7a013419acb47dc117aaccb6487622"})

response_raw = urllib2.urlopen(request)
response_cont = json.load(response_raw)
num_pages = int(response_cont['meta']['pagination']['total_pages'])
cur_page = int(response_cont['meta']['pagination']['current_page'])
remaining = int(response_raw.info().getheader('X-RateLimit-Remaining'))
reset_time = int(response_raw.info().getheader('X-RateLimit-Reset'))
next_url = str(response_cont['meta']['pagination']['links']['next'])

pages_left = num_pages - cur_page

add_to_dict(response_cont['data'])

while pages_left > 0: #second half
	if remaining == 0:
		wait_t = reset_time - int(time.time()) + 5
		print('   waiting for ' + str(wait_t) + ' seconds...    ')
		time.sleep(wait_t)
		print('done waiting')

	print(str(remaining)+' remaining...  num pages crawled: '+ str(cur_page) + " ... ")
	request = urllib2.Request(next_url, headers={"Content-Type" : "application/json", "X-API-Key" : "76935bbe4c7a013419acb47dc117aaccb6487622"})
	response_raw = urllib2.urlopen(request)
	response_cont = json.load(response_raw)
	cur_page = int(response_cont['meta']['pagination']['current_page'])
	remaining = int(response_raw.info().getheader('X-RateLimit-Remaining'))
	reset_time = int(response_raw.info().getheader('X-RateLimit-Reset'))
	if cur_page != num_pages:
		next_url = str(response_cont['meta']['pagination']['links']['next'])
		add_to_dict(response_cont['data'])

	pages_left = num_pages - cur_page

	

outfile = open('cannabis-reports-strains-1.json', 'w')
json.dump(all_data, outfile)
outfile.close()


