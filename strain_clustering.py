#Followed from http://brandonrose.org/clustering
from __future__ import print_function
import numpy as np
import pandas as pd
import nltk
import re
import os
import codecs
from sklearn import feature_extraction
import mpld3
import json
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.externals import joblib




def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token) and not token == '\xa0'.decode('windows-1252'):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems


def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token) and not token == '\xa0'.decode('windows-1252'):
            filtered_tokens.append(token)
    return filtered_tokens

#def main():
	# strains = json.load(open('consol_strains-3.json'))
	# stopwords = nltk.corpus.stopwords.words('english')
	# stemmer = SnowballStemmer("english")
strains = json.load(open('consol_strains-3.json'))
stopwords = nltk.corpus.stopwords.words('english')
stemmer = SnowballStemmer("english")
totalvocab_stemmed = []
totalvocab_tokenized = []
strain_names = []
descriptions = []
sources = []

for strain_name, entries in strains.iteritems():
	for i in range(0, len(entries)):
		cur = entries[i]
		descr = str(cur["description"])
		if len(descr) > 0:
			strain_names.append(strain_name)
			descriptions.append(descr)
			sources.append(str(cur["source"]))
		   	allwords_stemmed = tokenize_and_stem(descr) #for each item in 'synopses', tokenize/stem
		   	totalvocab_stemmed.extend(allwords_stemmed) #extend the 'totalvocab_stemmed' list
		    
		   	allwords_tokenized = tokenize_only(descr)
		   	totalvocab_tokenized.extend(allwords_tokenized)

vocab_frame = pd.DataFrame({'words': totalvocab_tokenized}, index = totalvocab_stemmed)
print('there are ' + str(vocab_frame.shape[0]) + ' items in vocab_frame')


tfidf_vectorizer = TfidfVectorizer(max_df=0.75, max_features=200000,
                                 min_df=0.15, stop_words='english',
                                 use_idf=True, tokenizer=tokenize_and_stem, ngram_range=(1,3))

tfidf_matrix = tfidf_vectorizer.fit_transform(descriptions) #fit the vectorizer to synopses

print(tfidf_matrix.shape)

terms = tfidf_vectorizer.get_feature_names()
dist = 1 - cosine_similarity(tfidf_matrix)

# num_clusters = 3

# km = KMeans(n_clusters=num_clusters)
# km.fit(tfidf_matrix)

# clusters = km.labels_.tolist()

# #uncomment the below to save your model 
# #since I've already run my model I am loading from the pickle

# joblib.dump(km,  'doc_cluster-5-1.pkl')

# #km = joblib.load('doc_cluster.pkl')
# #clusters = km.labels_.tolist()
# strains_dict = { 'strain': strain_names, 'description': descriptions, 'cluster': clusters, 'source': sources }

# frame = pd.DataFrame(strains_dict, index = [clusters] , columns = ['strain', 'cluster', 'source'])

# print("Top terms per cluster:")
# print()
# #sort cluster centers by proximity to centroid
# order_centroids = km.cluster_centers_.argsort()[:, ::-1] 

# for i in range(num_clusters):
#     print("Cluster %d words:" % i, end='')
    
#     for ind in order_centroids[i, :20]: #replace 6 with n words per cluster
#         print(' %s' % vocab_frame.ix[terms[ind].split(' ')].values.tolist()[0][0].encode('utf-8', 'ignore'), end=',')
#     print() #add whitespace
#     print() #add whitespace
    
#     print("Cluster %d strains:" % i, end='')
#     for strain in frame.ix[i]['strain'].values.tolist():
#         print(' %s,' % strain, end='')
#     print() #add whitespace
#     print() #add whitespace
    
# print()
# print()


################### HEIR. CLUSTERING 

linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances

fig, ax = plt.subplots(figsize=(50, 66)) # set size
ax = dendrogram(linkage_matrix, orientation="right", labels=strain_names);

plt.tick_params(\
    axis= 'x',          # changes apply to the x-axis
    which='both',      # both major and minor ticks are affected
    bottom='off',      # ticks along the bottom edge are off
    top='off',         # ticks along the top edge are off
    labelbottom='off')

plt.tight_layout() #show plot with tight layout

#uncomment below to save figure
plt.savefig('ward_clusters-2.png', dpi=200) #save figure as ward_clusters
plt.close()


#main()