---
layout:     post
title:      "Feature Engineering on Numeric Features"
subtitle:   "Feature Processing and Generation with respect to models"
date:       2018-01-25 12:00:00
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
## Feature Preprocessing

### Scaling

Scaling numeric features ensures that their initial impact on models are relatively the same.

### Winsorization or Rank Transformation to deal with Outliers

Outliers are not only exist in features but our target as well.

#### Winsorization

 To protect linear models from outliers, we can clip features values between two chosen values of lower bound and upper bound. We can choose them as some percentiles of that feature. For example, first and 99s percentiles. This procedure of clipping is known as winsorization

#### Rank Transformation

Rank transformation sets spaces between properly assorted values to be equal. It can be a better choice than MinMaxScaler if we have outliers bacause it moves outliers closer to normal objects.

There are 2 choice while applying rank transformation to the test set:

1. store the creative mapping from features values to their rank values
2. concatenate train and test sets before applying the rank transformation.

```python
scipy.stats.rankdata
```

### Log transformation

Log transformation acts as a representative of methametical transformations that often helps non-tree-based models and especially neural networks. As an alternative, you may extract a square root of the data. 

Both of these transformations can:
* drive extremely big values closer to the features' average value. 
* make values near zero to be more distinguishable. 

Despite the simplicity, one of these transformations can improve your neural network's results significantly. 

In conclusion, linear models, KNN, and neural networks can benefit hugely from this. 

## Feature Generation

Feature generation is a process of deriving new features using logic or knowledge derived after data exploration and hypothesis checking.

Examples:

1. Real Estate price and Real Estate squared area -> price per meter square
2. Horizontal distance and the vertical difference in heights -> direct distance.

Such examples can be of help not only for linear models. For example, although gradient within decision tree is a very powerful model, it still experiences difficulties with approximation of multiplications and divisions. And adding size features explicitly can lead to a more robust model with less amount of trees.

Apart from examples like adding, multiplications, divisions, and other features interactions, we can also:

3. A new feature indicating fractional part of these prices. For example, if some product costs 2.49, the fractional part of its price is 0.49. This feature can help the model utilize the differences in people's perception of these prices.

Also, we can find similar patterns in tasks which require distinguishing between a human and a robot. For example, if we will have some kind of financial data like auctions, we could observe that people tend to set round numbers as prices, and there are something like 0.935, blah, blah,, blah, very long number here. Or, if we are trying to find spambots on social networks, we can be sure that no human ever read messages with an exact interval of one second.

{% endcapture %}
{{ about_en | markdownify }}
</div>

<div class="en post-container">

</div>
