import json

data = json.load(open('leaves.json'))

labels = data['labels']
leaves = data['leaves']

for i in range(0, len(leaves)):
	if leaves[i] > 4730:
		print(str(leaves[i]))
		print(labels[leaves[i]])