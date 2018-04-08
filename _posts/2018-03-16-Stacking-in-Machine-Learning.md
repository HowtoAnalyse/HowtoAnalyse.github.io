---
layout: post
title: Stacking in Machine Learning
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo-236670.jpeg
featured: False
---

There are methods that are common in machine learning projects like cross validation, grid searching and stacking.

So I wrapped them into a common module in helper.py. 

In this script, I will call those functions directly. Feel free to have a check at my github for source code.




```python
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR, LinearSVR
from sklearn.kernel_ridge import KernelRidge
from xgboost import XGBRegressor

import numpy as np
import pandas as pd

```

    /Users/zxy/anaconda/envs/py35/lib/python3.5/site-packages/sklearn/cross_validation.py:41: DeprecationWarning: This module was deprecated in version 0.18 in favor of the model_selection module into which all the refactored classes and functions are moved. Also note that the interface of the new CV iterators are different from that of this module. This module will be removed in 0.20.
      "This module will be removed in 0.20.", DeprecationWarning)


Here is a tip for building your own module. 

During training, it's likely to do some modifications on the module file. We need to reload the module every time we have modified it.

Just as following ("helpers" is the name of module I built):


```python
import helpers
from importlib import reload
reload(helpers)
from helpers import *
```

## Load processed data

I have documented details of my data processing pipeline. Feel free to have a check on my blog.


```python
X = np.load("X.npy")
y = np.load("y.npy")
scaled_test = np.load("scaled_test.npy")
```


```python
models = [LinearRegression(),Ridge(),Lasso(alpha=0.01,max_iter=10000),RandomForestRegressor(),GradientBoostingRegressor(),SVR(),LinearSVR(),
          ElasticNet(alpha=0.001,max_iter=10000),SGDRegressor(max_iter=1000,tol=1e-3),BayesianRidge(),KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5),
          ExtraTreesRegressor(),XGBRegressor()]

names = ["LR", "Ridge", "Lasso", "RF", "GBR", "SVR", "LinSVR", "Ela","SGD","Bay","Ker","Extra","Xgb"]
for name, model in zip(names, models):
    score = rmse_cv(model, X, y)
    print("{}: {:.6f}, {:.4f}".format(name,score.mean(),score.std()))


```


```python
lasso_best = grid(Lasso()).grid_get(X,y,{'alpha': [0.0004,0.0005,0.0007,0.0006,0.0009,0.0008],'max_iter':[10000]})
```

    {'max_iter': 10000, 'alpha': 0.0005} 0.107202347338
                                     params  mean_test_score  std_test_score
    0  {'max_iter': 10000, 'alpha': 0.0004}         0.107326        0.003200
    1  {'max_iter': 10000, 'alpha': 0.0005}         0.107202        0.003151
    2  {'max_iter': 10000, 'alpha': 0.0007}         0.107412        0.003104
    3  {'max_iter': 10000, 'alpha': 0.0006}         0.107268        0.003121
    4  {'max_iter': 10000, 'alpha': 0.0009}         0.107871        0.003099
    5  {'max_iter': 10000, 'alpha': 0.0008}         0.107619        0.003103



```python
ridge_best=grid(Ridge()).grid_get(X,y,{'alpha':[35,40,45,50,55,60,65,70,80,90]})
```

    {'alpha': 35} 0.108637386149
              params  mean_test_score  std_test_score
    0  {'alpha': 35}         0.108637        0.003011
    1  {'alpha': 40}         0.108655        0.002995
    2  {'alpha': 45}         0.108684        0.002982
    3  {'alpha': 50}         0.108719        0.002972
    4  {'alpha': 55}         0.108761        0.002964
    5  {'alpha': 60}         0.108806        0.002958
    6  {'alpha': 65}         0.108855        0.002953
    7  {'alpha': 70}         0.108906        0.002950
    8  {'alpha': 80}         0.109014        0.002945
    9  {'alpha': 90}         0.109128        0.002943



```python
svr_best = grid(SVR()).grid_get(X,y,{'C':[11,12,13,14,15],'kernel':["rbf"],"gamma":[0.0003,0.0004],"epsilon":[0.008,0.009]})

```

    {'gamma': 0.0004, 'epsilon': 0.008, 'C': 15, 'kernel': 'rbf'} 0.106137364476
                                                   params  mean_test_score  \
    0   {'gamma': 0.0003, 'epsilon': 0.008, 'C': 11, '...         0.106940   
    1   {'gamma': 0.0004, 'epsilon': 0.008, 'C': 11, '...         0.106369   
    2   {'gamma': 0.0003, 'epsilon': 0.009, 'C': 11, '...         0.106881   
    3   {'gamma': 0.0004, 'epsilon': 0.009, 'C': 11, '...         0.106355   
    4   {'gamma': 0.0003, 'epsilon': 0.008, 'C': 12, '...         0.106825   
    5   {'gamma': 0.0004, 'epsilon': 0.008, 'C': 12, '...         0.106260   
    6   {'gamma': 0.0003, 'epsilon': 0.009, 'C': 12, '...         0.106781   
    7   {'gamma': 0.0004, 'epsilon': 0.009, 'C': 12, '...         0.106246   
    8   {'gamma': 0.0003, 'epsilon': 0.008, 'C': 13, '...         0.106715   
    9   {'gamma': 0.0004, 'epsilon': 0.008, 'C': 13, '...         0.106181   
    10  {'gamma': 0.0003, 'epsilon': 0.009, 'C': 13, '...         0.106698   
    11  {'gamma': 0.0004, 'epsilon': 0.009, 'C': 13, '...         0.106187   
    12  {'gamma': 0.0003, 'epsilon': 0.008, 'C': 14, '...         0.106623   
    13  {'gamma': 0.0004, 'epsilon': 0.008, 'C': 14, '...         0.106150   
    14  {'gamma': 0.0003, 'epsilon': 0.009, 'C': 14, '...         0.106607   
    15  {'gamma': 0.0004, 'epsilon': 0.009, 'C': 14, '...         0.106164   
    16  {'gamma': 0.0003, 'epsilon': 0.008, 'C': 15, '...         0.106535   
    17  {'gamma': 0.0004, 'epsilon': 0.008, 'C': 15, '...         0.106137   
    18  {'gamma': 0.0003, 'epsilon': 0.009, 'C': 15, '...         0.106500   
    19  {'gamma': 0.0004, 'epsilon': 0.009, 'C': 15, '...         0.106151   
    
        std_test_score  
    0         0.003543  
    1         0.003544  
    2         0.003533  
    3         0.003535  
    4         0.003526  
    5         0.003554  
    6         0.003526  
    7         0.003545  
    8         0.003523  
    9         0.003563  
    10        0.003527  
    11        0.003558  
    12        0.003528  
    13        0.003564  
    14        0.003527  
    15        0.003560  
    16        0.003534  
    17        0.003562  
    18        0.003532  
    19        0.003562  



```python
param_grid={'alpha':[0.2,0.3,0.4,0.5], 'kernel':["polynomial"], 'degree':[3],'coef0':[0.8,1,1.2]}
ker_best = grid(KernelRidge()).grid_get(X,y,param_grid)


```

    {'coef0': 1.2, 'kernel': 'polynomial', 'alpha': 0.3, 'degree': 3} 0.10715301547
                                                   params  mean_test_score  \
    0   {'coef0': 0.8, 'kernel': 'polynomial', 'alpha'...         0.108579   
    1   {'coef0': 1, 'kernel': 'polynomial', 'alpha': ...         0.107362   
    2   {'coef0': 1.2, 'kernel': 'polynomial', 'alpha'...         0.107167   
    3   {'coef0': 0.8, 'kernel': 'polynomial', 'alpha'...         0.110112   
    4   {'coef0': 1, 'kernel': 'polynomial', 'alpha': ...         0.107802   
    5   {'coef0': 1.2, 'kernel': 'polynomial', 'alpha'...         0.107153   
    6   {'coef0': 0.8, 'kernel': 'polynomial', 'alpha'...         0.111889   
    7   {'coef0': 1, 'kernel': 'polynomial', 'alpha': ...         0.108480   
    8   {'coef0': 1.2, 'kernel': 'polynomial', 'alpha'...         0.107397   
    9   {'coef0': 0.8, 'kernel': 'polynomial', 'alpha'...         0.113770   
    10  {'coef0': 1, 'kernel': 'polynomial', 'alpha': ...         0.109262   
    11  {'coef0': 1.2, 'kernel': 'polynomial', 'alpha'...         0.107748   
    
        std_test_score  
    0         0.003201  
    1         0.003276  
    2         0.003350  
    3         0.003130  
    4         0.003183  
    5         0.003245  
    6         0.003097  
    7         0.003131  
    8         0.003180  
    9         0.003082  
    10        0.003099  
    11        0.003137  



```python
ela_best = grid(ElasticNet()).grid_get(X,y,{'alpha':[0.0005,0.0008,0.004,0.005],'l1_ratio':[0.08,0.1,0.3,0.5,0.7],'max_iter':[10000]})
```

    {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio': 0.7} 0.107251756349
                                                   params  mean_test_score  \
    0   {'max_iter': 10000, 'alpha': 0.0005, 'l1_ratio...         0.112391   
    1   {'max_iter': 10000, 'alpha': 0.0005, 'l1_ratio...         0.111869   
    2   {'max_iter': 10000, 'alpha': 0.0005, 'l1_ratio...         0.109277   
    3   {'max_iter': 10000, 'alpha': 0.0005, 'l1_ratio...         0.107973   
    4   {'max_iter': 10000, 'alpha': 0.0005, 'l1_ratio...         0.107442   
    5   {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio...         0.110606   
    6   {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio...         0.110087   
    7   {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio...         0.107988   
    8   {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio...         0.107347   
    9   {'max_iter': 10000, 'alpha': 0.0008, 'l1_ratio...         0.107252   
    10  {'max_iter': 10000, 'alpha': 0.004, 'l1_ratio'...         0.107578   
    11  {'max_iter': 10000, 'alpha': 0.004, 'l1_ratio'...         0.107517   
    12  {'max_iter': 10000, 'alpha': 0.004, 'l1_ratio'...         0.109248   
    13  {'max_iter': 10000, 'alpha': 0.004, 'l1_ratio'...         0.111574   
    14  {'max_iter': 10000, 'alpha': 0.004, 'l1_ratio'...         0.112626   
    15  {'max_iter': 10000, 'alpha': 0.005, 'l1_ratio'...         0.107584   
    16  {'max_iter': 10000, 'alpha': 0.005, 'l1_ratio'...         0.107669   
    17  {'max_iter': 10000, 'alpha': 0.005, 'l1_ratio'...         0.110322   
    18  {'max_iter': 10000, 'alpha': 0.005, 'l1_ratio'...         0.112269   
    19  {'max_iter': 10000, 'alpha': 0.005, 'l1_ratio'...         0.113654   
    
        std_test_score  
    0         0.003620  
    1         0.003571  
    2         0.003351  
    3         0.003292  
    4         0.003221  
    5         0.003449  
    6         0.003396  
    7         0.003274  
    8         0.003195  
    9         0.003124  
    10        0.003153  
    11        0.003139  
    12        0.003104  
    13        0.003132  
    14        0.003148  
    15        0.003122  
    16        0.003103  
    17        0.003101  
    18        0.003143  
    19        0.003150  



```python
bay = BayesianRidge()
```

## Stacking


```python
lasso = Lasso(alpha=0.0005,max_iter=10000)
ridge = Ridge(alpha=60)
svr = SVR(gamma= 0.0004,kernel='rbf',C=13,epsilon=0.009)
ker = KernelRidge(alpha=0.2 ,kernel='polynomial',degree=3 , coef0=0.8)
ela = ElasticNet(alpha=0.005,l1_ratio=0.08,max_iter=10000)
bay = BayesianRidge()
```


```python
# stack_model = stacking(mod=[lasso_best,ridge_best,svr_best,ker_best,ela_best,bay],meta_model=ker_best)
stack_model = stacking(mod=[lasso,ridge,svr,ker,ela,bay],meta_model=ker)
print(rmse_cv(stack_model,X,y))

```

    [ 0.10162302  0.10740187  0.11592729  0.09769622  0.10343146]



```python
X_train_stack, X_test_stack = stack_model.get_oof(X,y,scaled_test)
X_train_add = np.hstack((X,X_train_stack))
X_test_add = np.hstack((scaled_test,X_test_stack))
print(rmse_cv(stack_model,X_train_add,y))


```

    [ 0.09625364  0.10155954  0.11045188  0.09230963  0.09976153]


## Finally!


```python
stack_model.fit(X,y)
```




    stacking(meta_model=KernelRidge(alpha=0.2, coef0=0.8, degree=3, gamma=None, kernel='polynomial',
          kernel_params=None),
         mod=[Lasso(alpha=0.0005, copy_X=True, fit_intercept=True, max_iter=10000,
       normalize=False, positive=False, precompute=False, random_state=None,
       selection='cyclic', tol=0.0001, warm_start=False), Ridge(alpha=60, copy_X=True, fit_intercept=True, max_iter=None,
       normalize=False, random_state=No...True, lambda_1=1e-06, lambda_2=1e-06, n_iter=300,
           normalize=False, tol=0.001, verbose=False)])




```python
pred = np.exp(stack_model.predict(scaled_test))
```


```python
sub=pd.read_csv("sample_submission.csv")
sub.tail(1)
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Id</th>
      <th>SalePrice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1458</th>
      <td>2919</td>
      <td>187741.866657</td>
    </tr>
  </tbody>
</table>
</div>




```python
from time import gmtime, strftime
submName = strftime("%Y%m%d%H%M%S", gmtime()) + '_submission.csv'
sub['SalePrice']=pred
sub.to_csv(submName, index=False)
```


