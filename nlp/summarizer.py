import re

# this is a naive text summarizer
# it works by finding the single sentence
# that has the most words in common with
# other sentences (eg in a review or description)

sample = "Cannabis is often used for its mental and physical effects, such as a high or stoned feeling, a general change in perception, euphoria (heightened mood), and an increase in appetite.[17][18] Short term side effects may include a decrease in short-term memory, dry mouth, impaired motor skills, red eyes, and feelings of paranoia or anxiety.[17][19][20] Long term side effects may include addiction, decreased mental ability in those who started as teenagers, and behavioral problems in children whose mothers used cannabis during pregnancy.[17] Onset of effects is within minutes when smoked and about 30 to 60 minutes when cooked and eaten.[17][21] They last for between two and six hours.Cannabis is mostly used recreationally or as a medicinal drug. It may also be used for religious or spiritual purposes. In 2013, between 128 and 232 million people used cannabis (2.7% to 4.9% of the global population between the ages of 15 and 65).[22] In 2015, 43% of Americans had used cannabis, which increased to 51% in 2016.[23] About 12% have used it in the past year, and 7.3% have used it in the past month.[24] This makes it the most commonly used illegal drug both in the world and the United States."

def summarize(text):
	text = text.replace('\n','.')
	sentences = text.split('.')

	rankings = rankSentences(sentences)
	summary = ""
	bestScore = 0
	for key in rankings:
		if rankings[key] > bestScore:
			bestScore = rankings[key]
			summary = key

	return summary

def rankSentences(sentences):
	n = len(sentences)
	# n by n matrix of 0s
	# which will store the word set intersection between sentences
	values = [[0 for x in range(n)] for x in range(n)]
	for i in range(n):
		for j in range(n):
			values[i][j] = calcIntersection(sentences[i],sentences[j])

	rankings = {} # maps sentence to score, score
	for i in range(n):
		score = 0
		for j in range(n):
			if i==j:
				continue
			score += values[i][j]

		rankings[sentences[i]] = score

	return rankings

def calcIntersection(s1, s2):
	words1 = set(s1.split(' '))
	words2 = set(s2.split(' '))
	inter = words1.intersection(words2)
	return len(inter)

# print summarize(sample)