---
date: 2018-01-15
title: Default Parameter Values
description: Default Parameter Values in Python
type: Document
categories:
  - Python
---

Let's have an example of what this post is going to talk about:



```python
def foo(a=[]):
    a.append(5)
    return a
```


```python
foo()
```




    [5]




```python
foo()
```




    [5, 5]




```python
foo()
```




    [5, 5, 5]



This happens because

> Default parameter values are evaluated when the function definition is executed. 

This means that the expression is evaluated once, when the function is defined, and that the same “pre-computed” value is used for each call. 

This is especially important to understand when a default parameter is a mutable object, such as a list or a dictionary: if the function modifies the object (e.g. by appending an item to a list), the default value is in effect modified. 

A way around this is to use None as the default, and explicitly test for it in the body of the function.

```python
def foo(a=None):
    if a==None:
        a=[]
    else:
        a.append(5)
    return a
```


```python
foo()
```




    []




```python
foo()
```




    []




```python
foo()
```




    []


