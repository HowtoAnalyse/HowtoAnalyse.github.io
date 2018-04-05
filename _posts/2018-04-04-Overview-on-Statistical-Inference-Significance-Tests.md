---
layout: post
title: Overview on Statistical Inference -- Significance Tests
author: sara
categories: [Data Science]
image: assets/images/dogs/pexels-photo.jpg
featured: True
---

There are two methods to make inferences about populations using sample data:

1. confidence intervals
2. significance tests

Both methods utilize the sampling distribution of the estimator of the parameter.

A confidence interval provides a range of plausible values for a parameter. 

A significance test judges whether a particular value for the parameter is plausible. This post provides a thorough overview on it.

## Summary table
| Parameter                                                  | Mean                                                                                                                              | Proportion                                                                                                                        |
|------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------|
| 1. Assumptions                                             | Random sample, quantitative parameter, normal distribution                                                                        | Random sample,  categorical parameter, no requirement on distribution for large samples                                           |
| 2. $H_0$ and $H_{\alpha}$: Null and alternative hypotheses | $$H_0: \mu = \mu_0$$ One sided: $$H_{\alpha}: \mu != \mu_0$$ Two sided: $$H_{\alpha}: \mu != \mu_0$$ $$H_{\alpha}: \mu != \mu_0$$ | $$H_0: \pi = \pi_0$$ One sided: $$H_{\alpha}: \pi != \pi_0$$ Two sided: $$H_{\alpha}: \pi != \pi_0$$ $$H_{\alpha}: \pi != \pi_0$$ |
| 3. A test statistic                                        | $$t=\frac{\bar{y}-\mu_0}{se}$$ with $se=\frac{s}{\sqrt{n}},df=n-1$                                                                | $$z=\frac{\hat{\pi}-\pi_0}{se_0}$$ with $se_0 = \sqrt{\pi_0(1-\pi_0)/n}$                                                          |
| 4. The P-value                                              <td colspan=2>The probability that the test statistic equals the observed value (one-sided) or a value even more extreme (two-sided)                                                                                                                                         
| 5. Conclusions                                             <td colspan=2>Reject $H_0$ if P-value $\leq \alpha$ such as 0.05                                                                                                                                                                                                         
Following are more detailed illustration on the 5 parts of significance tests:

### Assumptions

Tests assume that we have random sample. 

Tests for means apply with quantitative variables. Such tests use the t distribution which assumes that the population distribution is normal. In practice, two-sided tests like confidence intervals are robust to violations of the normality assumption.

Tests for proportions apply with categorical variables. Since the Central Limit Theorem implies approximate normality of the sampling distribution of the sample proportion, large-sample ones about proportions do not have requirement on population distribution.

>A statistical method is __robust__ if it performs adquately even when an assumption is violated.

Two-sided t tests and confidence intervals are robust against violations of the normal population assumption while one-sided test doesn't work well when n is small and the population distribution is highly skewed.

### $H_0$ and $H_{\alpha}$

$\mu_0$ and $\pi_0$ denote values hypothesized for the parameters. 

One-sided alternative hypothesis help to detect departures from $H_0$ in a particular direction. In most research articles, significance tests use two-sided P-values so that researchers avoid the suspicion that they chose $H_a$ when they saw the direction in which the data occurred, which is not ethical.

### Test statistic

A test statistics describes how far the estimated point falls from the $H_0$ value. The t statistic for means and z statistic for proportions measure the number of standard errors that the estimated point falls from the $H_0$ value.

## Decisions and Types of Errors

$\alpha$-level is also called the significance level. Common choices are 0.05 and 0.01. By choosing an $\alpha = 0.05$, we consider $P \leq 0.05$ as an evidence against $H_0$ strong enough to reject it.

When making a decision, there are 2 types of error we are likely to make:


|             | Reject $H_0$ | Not reject $H_0$ |
|-------------|--------------|------------------|
| $H_0$ True  | Type I error |                  |
| $H_0$ False |              | Type II error    |

From the table above, we could know that the probability of a Type I error is the $\alpha$-level for the test.

