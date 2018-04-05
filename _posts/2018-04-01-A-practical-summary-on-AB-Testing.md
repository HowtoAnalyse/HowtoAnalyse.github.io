---
layout: post
title: A practical summary on AB Testing
author: sara
categories: [Data Science]
image: assets/images/dogs/pexels-photo-289446.jpeg
featured: True
---
# Context

As a data analyst, statistical inference and hypothesis testing are ingrained in my daily work, and controlled experiments are used heavily in back-end algorithms in terms of recommendations and search relevance. An appreciation of randomness informs much of our decision making.

However, **on-line** A/B tests **at scale** present challenges not common in traditional experiments of human preference.

Here I'm going to review AB testing in a web environment for later reference:

1. Statistical power and sample size
2. Best practices
3. Performance Metrics

## Statistical power and sample size

In online experiementation platforms, we choose experiments with significant successful OECs to launch to the product.

The following formula approximates the desired sample size with confidence level at 95% and power as 90%:

$$n = (\frac{4r\sigma}{\delta})^2$$

where r is the number of variants, $$\sigma$$ is the standard deviation of the OEC and $$\delta$$ is the minimum difference between the OECs.

#### Power. 

Statistical power of a binary hypothesis test is the probability that the test correctly rejects the null hypothesis $$(H_0)$$ when a specific althernative hypothesis ($$H_1$$) is true. Commonly set to be around 80-95%. 

$$Power = Pr(\text{reject }H_0 | H_1\text{ is true})$$

It is reversely related to Type II error (False negative).

#### Confidence level

A confidence level at 95% implies that we will make Type I error (False positive) 5% of the time.

#### How to reduce Standard Error

A smaller standard error indicates a more powerful statistical test. There are 3 methods useful to reduce it:

1. **Choose OEC with inherently lower variability.** For example: conversion rate has lower sd than purchase count, which in turn has lower sd than revenue.

2. **Increase the sample size.** It usually **doesn't work well in practice**. Because larger sample size requires longer experiment period, which is not a desired requirement for a platform with strong seasonality.

3. **Detect noise and filter them out.** It usually adds up variability of the OEC to include users who are not directly involved in experiments, like those who have not visited the page you are testing on.

## Best Practices

Conducting a controlled experiment on apps or websites can be divided into 3 steps:

1. Randomization: mapping users to variants
2. Assignment: uses the output of the randomization to determine the experience that each user will see on the website
3. Data aggregation and analysis

#### Best Practice 1: Treatment Ramp-up

Before exposing a new feature to millions of users, we could start from a 99.9%/0.1% split and then increase the treatment size to 0.5% to 2.5%, etc., and finally 50%. It is suggested to run each step for a couple of hours.

#### Best Practice 2: Mine the data

User response is not the only data we have to determine where the difference in OEC is statistically significant. For example:

##### 1. System bug. 

An experiement showed no significant result. After data mining, you found that a population of users with a specific operating system version, say Android 8, response suspeciously worse for the treatment because there exists a bug of new feature for Android 8. What I will do is to exclude this population from analysis, and do a retesting once the bug is fixed.

##### 2. Seasonality

Traffic of online platforms, especially those in entertainment, shows clear patterns weekly or quaterly. It is suggested to do a preliminary exploration on traffic data, and choose a period that is enough to represent your user population. It varies from one week to 3 months.

#### Best Practice 3: Run continuous A/A tests

No matter what assignment method is employed: server-side, API-side or client-side, there is a chance that traffic is not splitted properly. So A/A tests are worth conducting to check whether the results are non-significant 95% of the time, traffic has been splitted according the expected percentages, etc.

Additionally, the variability of OECs of A/A tests can help determine the minimum sample size.

[//]: # (Performance Metrics)



# Reference

* [Kohavi, Ron, Randal M. Henne, and Dan Sommerfield. "Practical Guide to Controlled Experiments on the Web: Listen to Your Customers not to the HiPPO." (2007).](http://ai.stanford.edu/users/ronnyk/2007GuideControlledExperiments.pdf)

* [Selection Bias in Online Experimentation](https://medium.com/airbnb-engineering/selection-bias-in-online-experimentation-c3d67795cceb)
