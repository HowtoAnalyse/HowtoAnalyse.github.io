---
layout:     post
date: 2018-01-15 12:00:00
title: "Two layer neural network"
subtitle: "Implement a shallow neural network using NumPy"
author:     "Hux"
header-img: "img/post-bg-nextgen-web-pwa.jpg"
header-mask: 0.3
catalog:    true
multilingual: true
tags:
  - Deep-Learning-with-Numpy
---

<div class="zh post-container">
{% capture about_en %}

```python
import utils
import numpy as np

# import inspect
# lines = inspect.getsourcelines(utils.load_data)
# print("".join(lines[0]))

# import importlib
# importlib.reload(utils)
# help(utils)

X,Y = utils.load_data("../Titanic/data.npy")
```

    X shape: (7, 891)
    y shape: (1, 891)



```python
def sigmoid(z):
    s = 1/(1+np.exp(-z))
    return s

def layer_sizes(X, Y):
    n_x = X.shape[0]
    n_y = Y.shape[0]
    return (n_x, n_y)

def initialize_parameters(n_x, n_h, n_y):    
    np.random.seed(2) # we set up a seed so that your output matches ours although the initialization is random.
    W1 = np.random.randn(n_h,n_x)*0.01
    b1 = np.zeros((n_h,1))
    W2 = np.random.randn(n_y,n_h)*0.01
    b2 = np.zeros((n_y,1))
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}    
    return parameters

def forward_propagation(X, parameters):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    Z1 = np.dot(W1,X)+b1
    A1 = np.tanh(Z1)
    Z2 = np.dot(W2,A1)+b2
    A2 = sigmoid(Z2)
    cache = {"Z1": Z1,
             "A1": A1,
             "Z2": Z2,
             "A2": A2}    
    return A2, cache

def compute_cost(A2, Y, parameters):
    m = Y.shape[1] # number of example
    W1 = parameters['W1']
    W2 = parameters['W2']
    logprobs = np.multiply(np.log(A2),Y)+np.multiply((1-Y),np.log(1-A2))
    cost = -np.sum(logprobs)/m
    cost = np.squeeze(cost)
    return cost

def backward_propagation(parameters, cache, X, Y):
    m = X.shape[1]
    W1 = parameters["W1"]
    W2 = parameters["W2"]
    A1 = cache["A1"]
    A2 = cache["A2"]
    dZ2 = A2-Y
    dW2 = np.dot(dZ2,A1.T)/m
    db2 = np.sum(dZ2,axis=1,keepdims=True)/m
    dZ1 = np.dot(W2.T,dZ2)*(1-np.power(A1,2))
    dW1 = np.dot(dZ1,X.T)/m
    db1 = np.sum(dZ1,axis=1,keepdims=True)/m
    grads = {"dW1": dW1,
             "db1": db1,
             "dW2": dW2,
             "db2": db2}    
    return grads

def update_parameters(parameters, grads, learning_rate = 1.2):
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    dW1 = grads["dW1"]
    db1 = grads["db1"]
    dW2 = grads["dW2"]
    db2 = grads["db2"]
    W1 = W1-learning_rate*dW1
    b1 = b1-learning_rate*db1
    W2 = W2-learning_rate*dW2
    b2 = b2-learning_rate*db2
    parameters = {"W1": W1,
                  "b1": b1,
                  "W2": W2,
                  "b2": b2}    
    return parameters

def nn_model(X, Y, n_h, num_iterations = 10000, print_cost=False):
    np.random.seed(3)
    n_x = layer_sizes(X, Y)[0]
    n_y = layer_sizes(X, Y)[1]
    parameters = initialize_parameters(n_x, n_h, n_y)
    W1 = parameters["W1"]
    b1 = parameters["b1"]
    W2 = parameters["W2"]
    b2 = parameters["b2"]
    for i in range(0, num_iterations):
        A2, cache = forward_propagation(X, parameters)
        cost = compute_cost(A2, Y, parameters)
        grads = backward_propagation(parameters, cache, X, Y)
        parameters = update_parameters(parameters, grads)
        if print_cost and i % 1000 == 0:
            print ("Cost after iteration %i: %f" %(i, cost))
    return parameters

def predict(parameters, X):
    A2, cache = forward_propagation(X,parameters)
    predictions = np.round(A2)
    return predictions
```


```python
parameters = nn_model(X, Y, n_h = 4, num_iterations = 10000, print_cost=True)
predictions = predict(parameters, X)
print ('Accuracy: %d' % float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100) + '%')
```

    Cost after iteration 0: 0.693124
    Cost after iteration 1000: 0.393405
    Cost after iteration 2000: 0.386318
    Cost after iteration 3000: 0.383217
    Cost after iteration 4000: 0.381450
    Cost after iteration 5000: 0.380165
    Cost after iteration 6000: 0.379095
    Cost after iteration 7000: 0.378206
    Cost after iteration 8000: 0.377509
    Cost after iteration 9000: 0.376949
    Accuracy: 83%



```python
hidden_layer_sizes = [1, 2, 3, 4, 5, 20, 50]
for i, n_h in enumerate(hidden_layer_sizes):
    parameters = nn_model(X, Y, n_h, num_iterations = 5000)
    predictions = predict(parameters, X)
    accuracy = float((np.dot(Y,predictions.T) + np.dot(1-Y,1-predictions.T))/float(Y.size)*100)
    print ("Accuracy for {} hidden units: {} %".format(n_h, accuracy))
```

    Accuracy for 1 hidden units: 78.78787878787878 %
    Accuracy for 2 hidden units: 80.58361391694724 %
    Accuracy for 3 hidden units: 83.5016835016835 %
    Accuracy for 4 hidden units: 83.27721661054994 %
    Accuracy for 5 hidden units: 83.9506172839506 %
    Accuracy for 20 hidden units: 86.19528619528619 %
    Accuracy for 50 hidden units: 87.09315375982042 %



{% endcapture %}
{{ about_en | markdownify }}
</div>

<div class="en post-container">

</div>
