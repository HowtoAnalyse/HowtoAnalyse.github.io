---
layout: post
title: Parameter Tuning
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo.jpg
featured: False
---
Found some good sources to learn hypterparameter tuning today. 


Basically, there are 3 approaches: 

1. Grid Search 

2. Random Search 

3. Bayesian optimization  

Grid search is the first method I have learned. But it is considered to be a slow and unintelligent way to go about hyperparameter tuning. 

Between random search and Bayesian optimization, it does not seem as if any one of them outperforms the other in general. But when training time is critical, Bayesian hyperparameter optimization is a better choice. It costs you less training steps to achieve a comparable result to random search.  

## Reference: 

https://arimo.com/data-science/2016/bayesian-optimization-hyperparameter-tuning/ 

https://github.com/JasperSnoek/spearmint 

 