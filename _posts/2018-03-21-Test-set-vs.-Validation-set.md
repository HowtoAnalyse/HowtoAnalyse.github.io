---
layout: post
title: Test set vs. Validation set
author: sara
categories: [Machine Learning]
image: assets/images/dogs/theme-candid-portraits-smile-woman-girl-40064.jpeg
featured: False
---

When you have a large data set, it's recommended to split it into 3 parts:

* Training set: This is used to build up our prediction algorithm. Our algorithm tries to tune itself to the quirks of the training data sets. In this phase we usually create multiple algorithms in order to compare their performances during the Cross-Validation Phase.

* Validation set: This data set is used to compare the performances of the prediction algorithms that were created based on the training set. We choose the algorithm that has the best performance.

* Test set: Now we have chosen our preferred prediction algorithm but we don't know yet how it's going to perform on completely unseen real-world data. So, we apply our chosen prediction algorithm on our test set in order to see how it's going to perform so we can have an idea about our algorithm's performance on unseen data.

Notes:

-It's very important to keep in mind that skipping the test phase is not recommended, because the algorithm that performed well during the validation phase doesn't really mean that it's truly the best one, because the algorithms are compared based on the cross-validation set and its quirks and noises.

-During the Test Phase, the purpose is to see how our final model is going to deal in the wild, so in case its performance is very poor we should repeat the whole process starting from the Training Phase.
