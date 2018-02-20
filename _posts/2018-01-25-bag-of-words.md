---
date: 2018-01-22
title: Bag of words
description: Feature Extraction I -- Bag of words
type: Document
categories:
  - Machine-Learning
---

If text and images are the only data we got, it's more convenient to apply specific approach for these types of data. 

The common scenario is that we have text or images as additional data set, we need to grasp different features that can be input to machine learning models as a complementary to our main data frame of samples and features.

## Bag of words (BOW)

Pipeline of applying BOW:
1. Preprocessing:
	Lowercase, stemming, lemmatization, stopwords
2. N-grams can help to use local context
3. Postprocessing: TF-IDF

### TF-IDF

Intuition: normalize data column-wise

```python
sklearn.feature_extraction.text.TfidfVectorizer
```

#### Term Frequency (TF)
```python
tf = 1/x.sum(axis=1)[:,None]
x = x*tf
```

### Inverse Document Frequency (IDF)
```python
idf = np.log(x.shape[0]/(x>0).sum(0))
x=x*idf
```

### N-grams

```python
sklearn.feature_extraction.text.CountVectorizer: 
Ngram_range, analyzer
```

If you have 28 unique symbols, the number of all possible combinations is 28x28

## Next: Embeddings

Embeddings like Word2Vec