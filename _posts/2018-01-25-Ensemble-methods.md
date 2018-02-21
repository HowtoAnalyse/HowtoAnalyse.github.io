---
layout:     post
title:      "Ensemble Learning"
subtitle:   "Bagging, boosting and stacking in machine learning"
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
Bagging and boosting are two families of ensemble methods.

Ensemble methods aim at combining the predictions of several base estimators built with a given learning algorithm in order to improve generalizability / robustness over a single estimator.

###### Bagging(short for Bootstrap Aggregating):

* build several base estimators independently and then to average their predictions.
* aim to decrease variance by generating additional data for training from the original dataset
* suitable for models with high variance low bias (complex models)
* Examples: Random forest, which develop fully grown trees (note that RF modifies the grown procedure to reduce the correlation between trees)

###### Boosting:

* build several base estimators sequentialy and one tries to reduce the bias of the combined estimator
* aim to decrease bias
* suitable for models with low variance high bias
* Examples:  Gradient boosting

{% endcapture %}
{{ about_en | markdownify }}
</div>

<div class="en post-container">

</div>