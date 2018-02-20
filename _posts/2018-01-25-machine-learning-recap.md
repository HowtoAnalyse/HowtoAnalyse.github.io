---
date: 2018-01-15
title: Machine Learning Recap
description: Top 4 families of machine learning algorithms -- Linear Model, Tree-based methods, k-Nearest Neighbors and Neural Nets
type: Document
categories:
  - Machine-Learning
---

## No Free Lunch Theorem

Basically, No Free Lunch Theorem states that there is no methods which outperform all others on all tasks. 

The reason behind is that every method relies on certain assumptions about data or task. If these assumptions fail, it will perform poorly. 

For us, this means that we cannot every competition with just a single algorithm. So it is important for us to have a clear mind map of various models based off different assumptions. 

Then let's start getting familiar with the four popular families of machine learning algorithms.

##  Linear Model

Linear models try to separate objects with a plane which divides space into two parts.

With 2 sets of points, it is quite intuitive to separate them using a line. This approach can be generalized for a higher dimensional space. This is the main idea behind linear models.

Logistic regression or SVM are all linear models withdifferent loss functions.

### Linear models are especially good for sparse high dimensional data.

## Tree-Based Methods

In general, tree-based models are very powerful and can be a good default method for tabular data.

Intuitively, a single decision tree can be considered as dividing space into boxes and approximating data with a constant inside of these boxes. It uses divide-and-conquer approach to recur sub-split spaces into sub-spaces. 

The way of true axis splits and corresponding constants produces several approaches for building decision trees. Moreover, such trees can be combined together in a lot of ways. All this leads to a wide variety of tree-based algorithms, most famous of them being random forest and Gradient Boosted Decision Trees. 

Scikit-Learn contains quite good implementation of random forest. For gradient boost decision trees, you may find XGBoost and LightGBM with higher speed and accuracy. 

## k-Nearest Neighbors (k-NN)

The intuition behind k-NN is very simple. Closer objects will likely to have same labels.

## Neural Networks

Neural Nets is a special class of machine learning models, which deserve a separate topic.