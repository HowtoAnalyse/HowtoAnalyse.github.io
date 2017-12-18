---
layout: page-fullwidth
title: "what does a typical data science workflow look like?"
subheadline: "a Python data analysis pipeline"
teaser: "what does a typical data science workflow look like"
permalink: "/ds/"
header:
   image_fullwidth: "header_roadmap_2.jpg"
---

<div class="row">
<div class="medium-4 medium-push-8 columns" markdown="1">
<div class="panel radius" markdown="1">
**Table of Contents**
{: #toc }
*  TOC
{:toc}
</div>
</div><!-- /.medium-4.columns -->

<div class="medium-8 medium-pull-4 columns" markdown="1">
## Translate problem into questions {#questions}

Thinking about and documenting the problem we're working on make data analysis more effective.

## Feature Engineerning {#quality}

1. Is there any missing value?

2. Are there any quirks with the data?

Visualization makes **outliers** and **errors** immediately stand out, whereas they might go unnoticed in a large table of numbers. So plot everything you can about the data at this stage.

* Scatterplot matrix

Scatterplot matrices plot the distribution of each column along the diagonal, and then plot a scatterplot matrix for the combination of each variable. 

After this stage, our data will be:

* properly encoded
* falls within the expected range defined using domain knowledge
* missing values are either imputed or dropped

### Testing our data

Something like the following:

```python
assert len(df.loc[(df[col1].isnull()) |
                    (df[col2].isnull())]) == 0
```

### Exploratory analysis {#eda}

* How is my data distributed?
    - Box plots
    - Violin plots: contain the same information as box plots, and scales the box according to the density as well
* Are there any correlations in my data?
* Are there any confounding factors that explain these correlations?

Usually I do Stage 2 and 3 in the mean time.

## Modelling {#model}

### Classification
 - Tree methods
### Regression
### Unsupervised Learning

[Cross-validation]({{ site.url }}{{ site.baseurl }}/ds/validation/): k-fold 

Parameter tuning: Grid search

</div><!-- /.medium-8.columns -->
</div><!-- /.row -->