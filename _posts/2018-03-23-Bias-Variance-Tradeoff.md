---
layout: post
title: Bias Variance Tradeoff
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo-58997.jpeg
featured: False
---

In short, 
* bias is how far away a model's predictions are from true values, 
* variance is how scattered these predictions are among model iterations.

![jpg](/images/bias-and-variance.jpg)


> 
Error due to Bias: The error due to bias is taken as the difference between the expected (or average) prediction of our model and the correct value which we are trying to predict. Of course you only have one model so talking about expected or average prediction values might seem a little strange. However, imagine you could repeat the whole model building process more than once: each time you gather new data and run a new analysis creating a new model. Due to randomness in the underlying data sets, the resulting models will have a range of predictions. Bias measures how far off in general these models' predictions are from the correct value.
<cite>Scott Fortmann-Roe</cite>


>
Error due to Variance: The error due to variance is taken as the variability of a model prediction for a given data point. Again, imagine you can repeat the entire model building process multiple times. The variance is how much the predictions for a given point vary between different realizations of the model.
<cite>Scott Fortmann-Roe</cite>
