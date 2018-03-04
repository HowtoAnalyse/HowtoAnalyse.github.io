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

$$Power = Pr(reject H_0 | H_1 is true)$$

It is reversely related to Type II error (False negative).

#### Confidence level

A confidence level at 95% implies that we will make Type I error (False positive) 5% of the time.

#### How to reduce Standard Error

A smaller standard error indicates a more powerful statistical test. There are 3 methods useful to reduce it:

1. Choose OEC with inherently lower variability. For example: conversion rate has lower sd than purchase count, which in turn has lower sd than reevenue.

2. Increase the sample size.

It usually **doesn't work well in practice**. Because larger sample size requires longer experiment period, which is not a desired requirement for a platform with strong seasonality.

3. Detect noise and filter them out

It usually adds up variability of the OEC to include users who are not directly involved in experiments, like those who have not visited the page you are testing on.

## Best Practices

Conducting a controlled experiment on apps or websites can be divided into 3 steps:

### 1. Randomization

Randomization refers to the process that maps users to variants.

### 2. Assignment

Assignment step uses the output of the randomization to determine the experience that each user will see on the website.

#### Treatment Ramp-up

Before exposing a new feature to millions of users, we could start from a 99.9%/0.1% split and then increase the treatment size to 0.5% to 2.5%, etc., and finally 50%. It is suggested to run each step for a couple of hours.

### 3. Data aggregation and analysis


## Performance Metrics



# Reference

* [Kohavi, Ron, Randal M. Henne, and Dan Sommerfield. "Practical Guide to Controlled Experiments on the Web: Listen to Your Customers not to the HiPPO." (2007).](http://ai.stanford.edu/users/ronnyk/2007GuideControlledExperiments.pdf)

* [Selection Bias in Online Experimentation](https://medium.com/airbnb-engineering/selection-bias-in-online-experimentation-c3d67795cceb)
