---
layout: page-fullwidth
title: "Theme Documentation"
subheadline: "How to use Feeling Responsive"
teaser: "The documentation is a work in progress..."
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

## what is regularization and why it is useful. 

It is used to prevent overfitting: improve the generalization of a model
Decreases complexity of a model

### What are the benefits and drawbacks of specific methods, such as ridge regression and lasso?

Ridge regression:

We use an L2L2 penalty when fitting the model using least squares
We add to the minimization problem an expression (shrinkage penalty) of the form λ×∑coefficientsλ×∑coefficients
λλ: tuning parameter; controls the bias-variance tradeoff; accessed with cross-validation
A bit faster than the lasso
β̂ ridge=argminβ{∑ni=1(yi−β0−∑pj=1xijβj)2+λ∑pj=1β2j}β^ridge=argminβ{∑i=1n(yi−β0−∑j=1pxijβj)2+λ∑j=1pβj2}
The Lasso:

We use an L1L1 penalty when fitting the model using least squares
Can force regression coefficients to be exactly: feature selection method by itself
β̂ lasso=argminβ{∑ni=1(yi−β0−∑pj=1xijβj)2+λ∑pj=1||βj||}β^lasso=argminβ{∑i=1n(yi−β0−∑j=1pxijβj)2+λ∑j=1p||βj||}


</div><!-- /.medium-8.columns -->
</div><!-- /.row -->

 [1]: http://kramdown.gettalong.org/converter/html.html#toc
 [2]: {{ site.url }}/blog/
 [3]: http://srobbin.com/jquery-plugins/backstretch/
 [4]: #
 [5]: #
 [6]: #
 [7]: #
 [8]: #
 [9]: #
 [10]: #