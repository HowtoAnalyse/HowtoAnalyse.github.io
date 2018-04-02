---
layout: post
title: Feature Extraction
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo-179107.jpeg
featured: False
---
Feature extraction (Tokens => Features)

1. BOW: does not preserve ordering
2. n-grams: too many features => 
high frequency n-grams: stop-words and they won't help us to discriminate texts

Low frequency n-grams like typos may lead to overfit because our classifier can learn some independencies that are not there.

3. TF-IDF

### Term frequency (TF)

tf(t,d) -- frequency for term (or n-gram) t in document d
Variants:
weighting scheme| TF weight
binary | 0,1
raw count | f_{t,d}
term frequency | f_{t,d} / \sum{f_{t^',d}}
log normalization | 1+log(f_{t,d})

### Inverse document frequency (IDF)

N = |D| - total number of documents in corpus
|{d\belong D: t \belong d}| - number of documents where the term t appears
idf(t,D) = log\frac{N}{|{d\belon D:t\belong d}|}

### TF-IDF

tfidf(t,d,D) = tf(t,d)\times idf(t,D)

A high weight in TF-IDF is reached by a high term frequency in the given document while a low document frequency of the term in the whole collection of documents.

BOW + TF-IDF

1. replace counters with TF-IDF
2. Normalize the result row-wise (divide by L_2-norm)

Sentiment classification

Features:
bag of 1-grams with TF-IDF values
Models:
For such sparse features, Naive Bayes and Linear models are faster than tree method (decision tree, gradient boosted trees) and work for millions of features.

Among linear classification modesl, we choose logistic regression here:
p(y=1|x)=\sigma(w^Tx)
can handle sparse data, fast to train, weights can be interpreted

+ n-grams, throw away n-grams seen less than 5 times

Improvements: lr over bag of 1,2-grams with tf-idf




nlp gcp d3 stat scrapy

