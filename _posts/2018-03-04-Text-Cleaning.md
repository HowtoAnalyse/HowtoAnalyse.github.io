---
layout: post
title: Text Cleaning
author: sara
categories: [Machine Learning]
image: assets/images/dogs/dog-training-joy-fun-159692.jpeg
featured: False
---
Data cleaning and normalization can largely improve the efficiency of text analysis while they also bring us challenges.

## Encoding

A string in Python is seen as a Unicode covering the number from 0 through 0x10FFFF(1,114,111 decimal). Then the sequence has to be represented as a set of bytes (values from 0 to 255) in memory. The rules for translating a Unicode string into a sequence of bytes are called encoding.

As a rule of thumb data should be always normalized to UTF-8, which can handle any type of character.

## Data Structure

List is not a efficient format for large datasets. I prefer pandas dataframe to store the data. It has several advantages such as :

1. Rows are indexed, so search operations become faster.
2. A row can contain multiple fields with metadata about verbatims, which are useful in analysis.
3. Optimized processing methods of different kind are available. We can also optimize our own processing by using functional programming.

Since datasets in pandas must fit into RAM memory, it is suggested to use SFrames for larger ones.