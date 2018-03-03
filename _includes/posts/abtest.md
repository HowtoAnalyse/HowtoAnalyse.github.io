# Context

As a data analyst, statistical inference and hypothesis testing are ingrained in my daily work, and controlled experiments are used heavily in back-end algorithms in terms of recommendations and search relevance. An appreciation of randomness informs much of our decision making.

However, **on-line** A/B tests **at scale** present challenges not common in traditional experiments of human preference.

Here I'm going to review AB testing in a web environment for later reference:

1. Statistical power and sample size
2. Extensions to basic controlled experiments and their limitations
3. Performance Metrics

## Statistical power and sample size

In online experiementation platforms, we choose experiments with significant successful OECs to launch to the product.

The following formula approximates the desired sample size with confidence level at 95% and power as 90%:

$$n = (\frac{4r\sigma}{\delta})^2$$

where r is the number of variants, $$\sigma$$ is the standard deviation of the OEC and $$\delta$$ is the minimum difference between the OECs.


## Extensions and Limitations

## Performance Metrics



# Reference

* [Kohavi, Ron, Randal M. Henne, and Dan Sommerfield. "Practical Guide to Controlled Experiments on the Web: Listen to Your Customers not to the HiPPO." (2007).](http://ai.stanford.edu/users/ronnyk/2007GuideControlledExperiments.pdf)

* [Selection Bias in Online Experimentation](https://medium.com/airbnb-engineering/selection-bias-in-online-experimentation-c3d67795cceb)