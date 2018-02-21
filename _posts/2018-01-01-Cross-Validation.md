---
layout:     post
title:      "Cross Validation"
subtitle:   "What is cross-validation and How to do it right
type: Document"
date:       2018-01-15 12:00:00
author:     "Sara"
header-img: "img/post-bg-nextgen-web-pwa.jpg"
header-mask: 0.3
catalog:    true
multilingual: true
tags:
  - Machine-Learning
---

<div class="zh post-container">
{% capture about_en %}
## What is cross-validation?

It's a model validation technique for assessing how the results of a statistical analysis will generalize to an independent data set. 

It's common to find that our model performs differently depending on the subset of the data it's trained on. This phenomenon is known as **overfitting**: The model is learning to classify the training set so well that it doesn't generalize and perform well on data it hasn't seen before.

So we split the original data set into k subsets, use one of the subsets as the testing set, and the rest of the subsets are used as the training set. This process is then repeated k times such that each subset is used as the testing set exactly once.

This process is what we called cross-validation.

Examples: leave-one-out cross validation, K-fold cross validation

### How to do it right?

Firstly, the training and validation data sets should be drawn from the same population.

predicting stock prices: trained for a certain 5-year period, it’s unrealistic to treat the subsequent 5-year a draw from the same population
common mistake: for instance the step of choosing the kernel parameters of a SVM should be cross-validated as well

### Bias-variance trade-off for k-fold cross validation

Leave-one-out cross-validation: gives approximately unbiased estimates of the test error since each training set contains almost the entire data set (n−1 observations).

But: we average the outputs of n fitted models, each of which is trained on an almost identical set of observations hence the outputs are highly correlated. Since the variance of a mean of quantities increases when correlation of these quantities increase, the test error estimate from a LOOCV has higher variance than the one obtained with k-fold cross validation

Typically, we choose k=5 or k=10, as these values have been shown empirically to yield test error estimates that suffer neither from excessively high bias nor high variance.

## Robust or accurate algorithms, how do you choose?

Simpler models are preferred if more complex models do not significantly improve the quality of the description for the observations.

Our ultimate goal is to design systems with good generalization capacity, that is, systems that correctly identify patterns in data instances not seen before. While the generalization performance of a learning system strongly depends on the complexity of the model assumed.

If the model is too simple, the system can only capture the actual data regularities in a rough manner. In this case, the system has poor generalization properties and is said to suffer from underfitting.

By contrast, if the model is too complex, the system can identify accidental patterns in the training data that need not be present in the test set. These spurious patterns can be the result of random fluctuations or of measurement errors during the data collection process. In this case, the generalization capacity of the learning system is also poor. The learning system is said to be affected by overfitting. Spurious patterns, which are only present by accident in the data, tend to have complex forms.

By the way, ensemble learning can help balancing bias/variance. Several weak learners together = strong learner.

## How do you select metrics?

### Classification

1. Recall / Sensitivity / True positive rate

2. Precision / Positive Predictive value

3. Specificity / True negative rate

4. Accuracy

5. ROC / AUC

ROC is a graphical plot that illustrates the performance of a binary classifier (SensitivitySensitivity Vs 1−Specificity1−Specificity or SensitivitySensitivity Vs SpecificitySpecificity). They are not sensitive to unbalanced classes.
AUC is the area under the ROC curve. Perfect classifier: AUC=1, fall on (0,1); 100% sensitivity (no FN) and 100% specificity (no FP)

6. Logarithmic loss

Punishes infinitely the deviation from the true value! It’s better to be somewhat wrong than emphatically wrong!

7. Misclassification Rate

8. F1-Score

### Regression

1. Mean Squared Error Vs Mean Absolute Error 

RMSE gives a relatively high weight to large errors. The RMSE is most useful when large errors are particularly undesirable.

The MAE is a linear score: all the individual differences are weighted equally in the average. MAE is more robust to outliers than MSE.

2. Root Mean Squared Logarithmic Error

RMSLE penalizes an under-predicted estimate greater than an over-predicted estimate (opposite to RMSE)

3. Weighted Mean Absolute Error

The weighted average of absolute errors. MAE and RMSE consider that each prediction provides equally precise information about the error variation, i.e. the standard variation of the error term is constant over all the predictions. Examples: recommender systems (differences between past and recent products)
{% endcapture %}
{{ about_en | markdownify }}
</div>

<div class="en post-container">

</div>