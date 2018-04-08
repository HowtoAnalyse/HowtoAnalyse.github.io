---
layout: post
title: PCA can do more than dimension reduction
author: sara
categories: [Machine Learning]
image: assets/images/dogs/pexels-photo-58997.jpeg
featured: False
---

I was at first inspired by a discussion on Kaggle forum that doing PCA helps obtain a big boost on leaderboard. 




```python
import numpy as np
from sklearn.preprocessing import RobustScaler, Imputer
from sklearn.decomposition import PCA

```


```python
piped = np.load("piped.npy")
y_raw = np.load("y_raw.npy")
```

When it comes to data transformation, we should always do the transformation on training and test set separately. Because when you train a classifier, you cannot use any information from the test set.


```python
train_X = scaled_pipe[:len(y_raw)]
test_X = scaled_pipe[len(y_raw):]
print("Shape of training X: {}".format(train_X.shape))
print("Shape of test X: {}".format(test_X.shape))
```

    Shape of training X: (1458, 427)
    Shape of test X: (1459, 427)



```python
scaler = RobustScaler()
scaled_train = scaler.fit(train_X).transform(train_X)
scaled_test = scaler.transform(test_X)

```

The appropriate way to apply PCA is to run it on the training set, save the principal components that you use, and then use them to transform the points in your test set. 

`fit_transform()` and `transform` functions in sklearn simplified code for us. 


```python
pca = PCA(n_components=410)
X_scaled=pca.fit_transform(scaled_train)
test_X_scaled = pca.transform(scaled_test)
```


```python
y_log = np.log(y_raw)
y_log.shape
```




    (1458,)




```python
X = Imputer().fit_transform(scaled_train)
y = Imputer().fit_transform(y_log.reshape(-1,1)).ravel()
```

Save the processed data for model training


```python
np.save("X",X)
np.save("scaled_test",scaled_test)
np.save("y",y)



```

