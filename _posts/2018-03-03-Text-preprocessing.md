---
layout: post
title: Text preprocessing
author: sara
categories: [Machine Learning]
image: assets/images/dogs/french-bulldog-summer-smile-joy-160846.jpeg
featured: False
---
Text preprocessing

# Tokenization

A token can be considered as a useful unit for semantic processing. It can be a word, sentence, paragraph, et.

Tokenization is a process that splits an input sequence into tokens.

1. TreebankWordTokenizer()

It uses the grammar rules of English to make it close to perfect tokenization for further analysis.

# Token normalization

## Stemming

Stem is the root form of the word. 

dogs -> dog
walked -> walk

Stemming is a process of removing and replacing suffixes to get the stem.
Howevery, it fails on irregular form like:

wolves -> wolv

## Lemmatization

After lemmatization, words are returned to their base.
However, it doesn't reduce all forms like:

talked -> talked 

In practice, we usually try them both and choose what works best for our task.

## Other normalization techniques

* Capital letters
* Acronyms

