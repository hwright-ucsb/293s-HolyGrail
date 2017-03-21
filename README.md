## 293s - Our Class Project



![python](https://img.shields.io/badge/Python-2.7.13%2B-437ebf.svg?colorA=96b2b4&style=flat-square)

![scrapy](https://img.shields.io/badge/Scrapy-1.3.2-437ebf.svg?colorA=96b2b4&style=flat-square)

![tensorflow](https://img.shields.io/badge/TensorFlow-1.0.0-437ebf.svg?colorA=96b2b4&style=flat-square)


# General Structure Of This Repository

# Data Collection & Data Cleaning
Scraping code can be found in the following directories:

cannabis-reports, morestrains, qannabis, scrapetest, wikileaf, strains420101, python_stuff

These mostly just include various Scrapy spiders. Instructions on how to run these can be found here: https://doc.scrapy.org/en/latest/intro/tutorial.html


The data_consol and leafly_reviews directories contain scripts to consolidate our data from our various sources.
We needed this because we didn't uniformly scrape data in the same format from each source.

data_consol has code to aggregate all the strain and strain descriptions together into one large json object.

leafly_reviews has code to match all the reviews to each strain we consolidated together in data_consol.
It also has some code to reconcile a few differences between information for a single strain. For instance, a review for strain X could have different attributes than strain X's description and attribute information.
We also have a script in here to calculate the "true" rating for a particular strain, since we noticed that Leafly's rating system was inaccurate.

# Data Analysis

Our data analysis code can be found in the following directories:

nlp, sklearn, tensorflow, data_consol

The data_consol directory contains code to calculate similarity between strain descriptions.

The nlp directory contains a Python script to summarize some text.

The sklearn directory contains several scripts to cluster our strains (we tried both hierarchical and kmeans)

The tensorflow directory contains the code we used for calculating term similarities (synonyms within our strain description and reviews)
