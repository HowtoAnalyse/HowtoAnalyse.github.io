---
date: 2018-01-15
title: DataFrame to Dictionary
description: Convert Pandas DataFrame to Dictionary
type: Document
categories:
  - Pandas
---

## `to_dict()` method

Consider the following simple DataFrame:


```python
import pandas as pd
df=pd.DataFrame(
{'Users':['a','b'],'Events':[5,75]},index=['0','1'])
df
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
      <th>Events</th>
      <th>Users</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>5</td>
      <td>a</td>
    </tr>
    <tr>
      <th>1</th>
      <td>75</td>
      <td>b</td>
    </tr>
  </tbody>
</table>
</div>



`to_dict()` converts it into a dictionary.


```python
df.to_dict()
```




    {'Events': {'0': 5, '1': 75}, 'Users': {'0': 'a', '1': 'b'}}



## Specify the return orientation

_dict_ is the default format as shown above.

In case a different dictionary format is needed, here are examples of the possible orient arguments:

**list** - Keys of the converted dictionary are columns names, values are lists of column data


```python
df.to_dict('list')
```




    {'Events': [5, 75], 'Users': ['a', 'b']}



**series** - like _list_ while values are Series


```python
df.to_dict('series')
```




    {'Events': 0     5
     1    75
     Name: Events, dtype: int64, 'Users': 0    a
     1    b
     Name: Users, dtype: object}



**split** - splits columns, data and index as keys


```python
df.to_dict('split')
```




    {'columns': ['Events', 'Users'],
     'data': [[5, 'a'], [75, 'b']],
     'index': ['0', '1']}



**records** - each row becomes a dictionary where key is the column name and value is the data in the cell


```python
df.to_dict('records')
```




    [{'Events': 5, 'Users': 'a'}, {'Events': 75, 'Users': 'b'}]



**index** - like `records`, but a dictionary of dictionaries with keys as index labels (rather than a list)


```python
df.to_dict('index')
```




    {'0': {'Events': 5, 'Users': 'a'}, '1': {'Events': 75, 'Users': 'b'}}




