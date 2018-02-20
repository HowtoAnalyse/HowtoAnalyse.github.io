---
date: 2018-01-22
title: Build a Recommender Engine with Gensim
description: Recoemmend to-read books using Gensim
type: Document
categories:
  - Recommender
---



Recommender engines powered by Word2Vec are able to learn user preference adaptively based on previous interactions.

This notebook gives an example using Gensim. 

For a more detailed implementation using Tensorflow >> https://howtoanalyse.github.io/recommender/Word2Vec/

## Step 1. Make every user's to-read list as a sentence and feed it into word2vec

Given a dataset large enough, it can find out similar books


```python
import pandas as pd
from gensim.models import Word2Vec, KeyedVectors
```


```python
tr = pd.read_csv( 'to_read.csv' )
b = pd.read_csv( 'books.csv' )
bt = tr.merge( b[[ 'book_id', 'title']], on = 'book_id' )
```


```python
bt.sample(10)
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
      <th>user_id</th>
      <th>book_id</th>
      <th>title</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>102338</th>
      <td>25663</td>
      <td>67</td>
      <td>A Thousand Splendid Suns</td>
    </tr>
    <tr>
      <th>631930</th>
      <td>25250</td>
      <td>7629</td>
      <td>Auschwitz</td>
    </tr>
    <tr>
      <th>790848</th>
      <td>32567</td>
      <td>5442</td>
      <td>Vicious (Villains, #1)</td>
    </tr>
    <tr>
      <th>475377</th>
      <td>9423</td>
      <td>6239</td>
      <td>Royal Blood (Vampire Kisses, #6)</td>
    </tr>
    <tr>
      <th>94525</th>
      <td>28268</td>
      <td>33</td>
      <td>Memoirs of a Geisha</td>
    </tr>
    <tr>
      <th>548850</th>
      <td>19543</td>
      <td>4290</td>
      <td>Whose Body?  (Lord Peter Wimsey, #1)</td>
    </tr>
    <tr>
      <th>652391</th>
      <td>28523</td>
      <td>649</td>
      <td>1Q84</td>
    </tr>
    <tr>
      <th>813174</th>
      <td>10051</td>
      <td>4499</td>
      <td>The Paris Architect</td>
    </tr>
    <tr>
      <th>831203</th>
      <td>39958</td>
      <td>1511</td>
      <td>The Slow Regard of Silent Things (The Kingkill...</td>
    </tr>
    <tr>
      <th>45407</th>
      <td>37147</td>
      <td>317</td>
      <td>I Know Why the Caged Bird Sings</td>
    </tr>
  </tbody>
</table>
</div>




```python
raw = bt.groupby('user_id')['title'].apply(list)
assert len(raw)==tr.user_id.nunique()
```


```python
sentences = [b for b in raw.values]
```


```python
model = Word2Vec(sentences, size=128, window=5, workers=4, min_count=5)
```


```python
print(model)
```

    Word2Vec(vocab=9676, size=128, alpha=0.025)



```python
words = list(model.wv.vocab)
```

## Step 2. Store and Query book vectors


```python
book_vectors = model.wv
```


```python
from time import gmtime, strftime
fname = 'vectors_' + strftime("%Y%m%d", gmtime())
```


```python
book_vectors.save(fname)
```


```python
old_vectors = KeyedVectors.load('vectors_20180220')
```

Say, a user bookmarked _A Hundred Summers_ and _The Stand_ on his to-do list and disliked _The Silver Star_, the recommendation engine will suggest a list of books as following:


```python
old_vectors.most_similar_cosmul(positive=['A Hundred Summers','The Stand'],negative=['The Silver Star'])
```




    [('Preludes & Nocturnes (The Sandman #1)', 1.1122468709945679),
     ('The Gods Themselves', 1.1107063293457031),
     ('Preacher, Volume 1: Gone to Texas', 1.1103928089141846),
     ('Snow Crash', 1.1093586683273315),
     ('Gateway (Heechee Saga, #1)', 1.109340786933899),
     ('Doomsday Book (Oxford Time Travel, #1)', 1.1071699857711792),
     ('The Fountains of Paradise', 1.1049118041992188),
     ('Sundiver (The Uplift Saga, #1)', 1.1040676832199097),
     ('Soon I Will Be Invincible', 1.1027390956878662),
     ('The Children of Húrin', 1.1015183925628662)]






