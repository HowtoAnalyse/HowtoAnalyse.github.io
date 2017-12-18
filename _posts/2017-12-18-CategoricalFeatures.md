---
layout: page
sidebar: right
title: "Feature Engineering"
subheadline: "Feature Engineering Part 1: Categorical and Ordinal features"
teaser: "Feature Preprocessing and generation with respect to models"
tags:
  - overview
categories:
  - Machine Learning
---

Ordinal features refer to ordered categorical features. Examples include 
* Driver's license: A,B,C,D
* Education level: Bachelor, Master, Doctoral
* ...

### Difference between Numeric and Ordinal Features with values 1,2,3...

For numerical features with values 1,2,3..., we can conclude that the distance between first, and the second class is equal to the distance between second and the third class, but because for ordinal features, we can't tell which distance is bigger. 

As these numeric features, we can't sort and integrate an ordinal feature the other way, and expect to get similar performance. 

### Encode a Categorical Feature

The simplest way to encode a categorical feature is to map it's unique values to different numbers.

This method works fine with two ways because tree-methods can split feature, and extract most of the useful values in categories on its own. 





