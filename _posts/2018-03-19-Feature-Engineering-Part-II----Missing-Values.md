---
layout: post
title: Feature Engineering Part II -- Missing Values
author: sara
categories: [Machine Learning]
image: assets/images/dogs/huskies-husky-blue-eye-dog-60050.jpeg
featured: False
---

## Imputation

a. Replace it with a number outside the normal range like -999 
b. Replace it with mean or median
c. Reconstruct values

Method a is useful because it gives trees the possibility to take missing values into a separate category. The downside is that performance of linear models and neural networks will suffer.

Method b is beneficial for simple linear models and neural networks. But tree-based methods can be harder to select object with missing values in the first place.

### Method c: Reconstruct values

When data points are dependent to each other like time series data, we can approximate NAs using observations in the neighborhood.

Challenges come when data points are independent.


## Feature Generation

Sometimes we create a binary feature, isnull, indicating which rows have missing values for this feature. Through this way, we can address concerns about trees and neural networks while computing mean or median. The drawback is that we will double the number of columns.

This method is especially worth trying for missing data occured in test set only. The intuition behind is that categories absent in the training set will be treated randomly eventually.

As an alternative, we may have a try on frequency encoding with missing values as a new category. 

## Xgboost can handle NaN. 


