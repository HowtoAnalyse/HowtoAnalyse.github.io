---
layout: page
sidebar: right
title: "Hypothesis Testing"
categories:
  - Statistical-Inference
tags:
  - Hypothesis-Testing
---

4 steps:
1. Null Hypothesis and Alternative hypotheses
Type I error -- rejecting a true null
Type II error -- declaring the plausibility of a false null

Also think about the type 1 error (rejecting a true null) and type 2 error (declaring the plausibility of a false null) possibilities at this time and how serious each mistake would be in terms of the problem.

2. Collect and summarize the data so that a test statistic can be calculated
A test statistic is a summary of the data that measures the difference between what is seen in the data and what would be expected if the null hypothesis were true. It is typically standardized so that a p-value can be obtained from a reference distribution like the normal curve.

3. 


```python
raw[raw['Gender']=='Male']['VIQ'].mean()
```




    115.25




```python
from scipy import stats
```


```python
## Normality test
stats.mstats.normaltest(raw['PIQ'])

```




    NormaltestResult(statistic=11.681588179999903, pvalue=0.0029065336598567129)




```python
raw.describe()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>FSIQ</th>
      <th>VIQ</th>
      <th>PIQ</th>
      <th>Weight</th>
      <th>Height</th>
      <th>MRI_Count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>40.000000</td>
      <td>40.000000</td>
      <td>40.000000</td>
      <td>40.00000</td>
      <td>38.000000</td>
      <td>39.000000</td>
      <td>4.000000e+01</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>20.500000</td>
      <td>113.450000</td>
      <td>112.350000</td>
      <td>111.02500</td>
      <td>151.052632</td>
      <td>68.525641</td>
      <td>9.087550e+05</td>
    </tr>
    <tr>
      <th>std</th>
      <td>11.690452</td>
      <td>24.082071</td>
      <td>23.616107</td>
      <td>22.47105</td>
      <td>23.478509</td>
      <td>3.994649</td>
      <td>7.228205e+04</td>
    </tr>
    <tr>
      <th>min</th>
      <td>1.000000</td>
      <td>77.000000</td>
      <td>71.000000</td>
      <td>72.00000</td>
      <td>106.000000</td>
      <td>62.000000</td>
      <td>7.906190e+05</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>10.750000</td>
      <td>89.750000</td>
      <td>90.000000</td>
      <td>88.25000</td>
      <td>135.250000</td>
      <td>66.000000</td>
      <td>8.559185e+05</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>20.500000</td>
      <td>116.500000</td>
      <td>113.000000</td>
      <td>115.00000</td>
      <td>146.500000</td>
      <td>68.000000</td>
      <td>9.053990e+05</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>30.250000</td>
      <td>135.500000</td>
      <td>129.750000</td>
      <td>128.00000</td>
      <td>172.000000</td>
      <td>70.500000</td>
      <td>9.500780e+05</td>
    </tr>
    <tr>
      <th>max</th>
      <td>40.000000</td>
      <td>144.000000</td>
      <td>150.000000</td>
      <td>150.00000</td>
      <td>192.000000</td>
      <td>77.000000</td>
      <td>1.079549e+06</td>
    </tr>
  </tbody>
</table>
</div>




```python
groupby_gender = raw.groupby('Gender')
for gender, value in groupby_gender['VIQ']:
    print((gender, value.mean()))
```

    ('Female', 109.45)
    ('Male', 115.25)
    


```python
groupby_gender.mean()
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Unnamed: 0</th>
      <th>FSIQ</th>
      <th>VIQ</th>
      <th>PIQ</th>
      <th>Weight</th>
      <th>Height</th>
      <th>MRI_Count</th>
    </tr>
    <tr>
      <th>Gender</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>Female</th>
      <td>19.65</td>
      <td>111.9</td>
      <td>109.45</td>
      <td>110.45</td>
      <td>137.200000</td>
      <td>65.765000</td>
      <td>862654.6</td>
    </tr>
    <tr>
      <th>Male</th>
      <td>21.35</td>
      <td>115.0</td>
      <td>115.25</td>
      <td>111.60</td>
      <td>166.444444</td>
      <td>71.431579</td>
      <td>954855.4</td>
    </tr>
  </tbody>
</table>
</div>




```python
%matplotlib inline

groupby_gender.boxplot(column=['FSIQ', 'VIQ', 'PIQ'])
```




    Female         Axes(0.1,0.15;0.363636x0.75)
    Male      Axes(0.536364,0.15;0.363636x0.75)
    dtype: object




![png](output_8_1.png)



```python
from pandas.tools import plotting
plotting.scatter_matrix(raw[['Weight', 'Height', 'MRI_Count']]) 
```




    array([[<matplotlib.axes._subplots.AxesSubplot object at 0x0000000010F2F240>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x00000000110C97F0>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x000000001110D048>],
           [<matplotlib.axes._subplots.AxesSubplot object at 0x0000000011158630>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x000000001116ECC0>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x00000000111EA470>],
           [<matplotlib.axes._subplots.AxesSubplot object at 0x0000000011234978>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x00000000112780F0>,
            <matplotlib.axes._subplots.AxesSubplot object at 0x00000000112C5518>]], dtype=object)




![png](output_9_1.png)


## Student's t-test
### 1-sample t-test
scipy.stats.ttest_1samp() tests if the population mean of data is likely to be equal to a given value (technically if observations are drawn from a Gaussian distributions of given population mean). It returns the T statistic, and the p-value (see the function’s help):


```python
stats.ttest_1samp(raw['VIQ'], 0)
```




    Ttest_1sampResult(statistic=30.088099970849328, pvalue=1.3289196468728067e-28)



With a p-value of 10^-28 we can claim that the population mean for the IQ (VIQ measure) is not 0.

### 2-sample t-test

We have seen above that the mean VIQ in the male and female populations were different. To test if this is significant, we do a 2-sample t-test with scipy.stats.ttest_ind():


```python
female_viq = raw[raw['Gender'] == 'Female']['VIQ']
male_viq = raw[raw['Gender'] == 'Male']['VIQ']
stats.ttest_ind(female_viq, male_viq)   

```




    Ttest_indResult(statistic=-0.77261617232750113, pvalue=0.44452876778583217)



## Paired tests: repeated measurements on the same individuals

PIQ, VIQ, and FSIQ give 3 measures of IQ. Let us test if FISQ and PIQ are significantly different. We can use a 2 sample test:


```python
stats.ttest_ind(raw['FSIQ'], raw['PIQ'])
```




    Ttest_indResult(statistic=0.46563759638096403, pvalue=0.64277250094148408)



**The problem with this approach is that it forgets that there are links between observations**: FSIQ and PIQ are measured on the same individuals. Thus the variance due to inter-subject variability is **confounding**, and can be removed, using a “paired test”, or “repeated measures test”:


```python
stats.ttest_rel(raw['FSIQ'], raw['PIQ']) 
```




    Ttest_relResult(statistic=1.7842019405859857, pvalue=0.082172638183642358)



This is **equivalent to a 1-sample test on the difference**:


```python
stats.ttest_1samp(data['FSIQ'] - data['PIQ'], 0)   

```

**T-tests assume Gaussian errors**. We can use a Wilcoxon signed-rank test, that relaxes this assumption:


```python
stats.wilcoxon(data['FSIQ'], data['PIQ'])   
```

 **The corresponding test in the non paired case is the Mann–Whitney U test**, scipy.stats.mannwhitneyu().

## Linear models, multiple factors, and analysis of variance

Given two set of observations, x and y, we want to test the hypothesis that y is a linear function of x. In other terms:

y = x * coef + intercept + e

where e is observation noise. We will use the statsmodels module to:

Fit a linear model. We will use the simplest strategy, ordinary least squares (OLS).
Test that coef is non zero.

### Categorical variables: comparing groups or multiple categories


```python
from statsmodels.formula.api import ols
model = ols("VIQ ~ Gender + 1", raw).fit()
print(model.summary()) 

```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                    VIQ   R-squared:                       0.015
    Model:                            OLS   Adj. R-squared:                 -0.010
    Method:                 Least Squares   F-statistic:                    0.5969
    Date:                Thu, 21 Dec 2017   Prob (F-statistic):              0.445
    Time:                        09:03:04   Log-Likelihood:                -182.42
    No. Observations:                  40   AIC:                             368.8
    Df Residuals:                      38   BIC:                             372.2
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ==================================================================================
                         coef    std err          t      P>|t|      [95.0% Conf. Int.]
    ----------------------------------------------------------------------------------
    Intercept        109.4500      5.308     20.619      0.000        98.704   120.196
    Gender[T.Male]     5.8000      7.507      0.773      0.445        -9.397    20.997
    ==============================================================================
    Omnibus:                       26.188   Durbin-Watson:                   1.709
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):                3.703
    Skew:                           0.010   Prob(JB):                        0.157
    Kurtosis:                       1.510   Cond. No.                         2.62
    ==============================================================================
    
    Warnings:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    

Forcing categorical: the ‘Gender’ is automatically detected as a categorical variable, and thus **each of its different values are treated as different entities**.

**An integer column can be forced to be treated as categorical using:**


```python
model = ols('VIQ ~ C(Gender)', raw).fit()
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-7-a922adb4b86f> in <module>()
    ----> 1 model = ols('VIQ ~ C(Gender)', raw).fit()
    

    NameError: name 'ols' is not defined


**Intercept**: We can remove the intercept using - 1 in the formula, or force the use of an intercept using + 1.

 By default, statsmodels treats a categorical variable with K possible values as K-1 ‘dummy’ boolean variables (the last level being absorbed into the intercept term). This is almost always a good default choice - however, it is possible to specify different encodings for categorical variables 

To compare different types of IQ, we need to create a “long-form” table, listing IQs, where the type of IQ is indicated by a categorical variable:


```python
data_fisq = pd.DataFrame({'iq': raw['FSIQ'], 'type': 'fsiq'})
data_piq = pd.DataFrame({'iq': raw['PIQ'], 'type': 'piq'})
data_long = pd.concat((data_fisq, data_piq))
model = ols("iq ~ type", data_long).fit()
print(model.summary())  
```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:                     iq   R-squared:                       0.003
    Model:                            OLS   Adj. R-squared:                 -0.010
    Method:                 Least Squares   F-statistic:                    0.2168
    Date:                Thu, 21 Dec 2017   Prob (F-statistic):              0.643
    Time:                        09:11:17   Log-Likelihood:                -364.35
    No. Observations:                  80   AIC:                             732.7
    Df Residuals:                      78   BIC:                             737.5
    Df Model:                           1                                         
    Covariance Type:            nonrobust                                         
    ===============================================================================
                      coef    std err          t      P>|t|      [95.0% Conf. Int.]
    -------------------------------------------------------------------------------
    Intercept     113.4500      3.683     30.807      0.000       106.119   120.781
    type[T.piq]    -2.4250      5.208     -0.466      0.643       -12.793     7.943
    ==============================================================================
    Omnibus:                      164.598   Durbin-Watson:                   1.531
    Prob(Omnibus):                  0.000   Jarque-Bera (JB):                8.062
    Skew:                          -0.110   Prob(JB):                       0.0178
    Kurtosis:                       1.461   Cond. No.                         2.62
    ==============================================================================
    
    Warnings:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    

We can see that we retrieve the same values for t-test and corresponding p-values for the effect of the type of iq than the previous t-test:


```python
stats.ttest_ind(data['FSIQ'], data['PIQ']) 
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-25-683d0187bfed> in <module>()
    ----> 1 stats.ttest_ind(data['FSIQ'], data['PIQ'])
    

    NameError: name 'data' is not defined


## Multiple Regression: including multiple factors
Consider a linear model explaining a variable z (the dependent variable) with 2 variables x and y:

z = x \, c_1 + y \, c_2 + i + e

Such a model can be seen in 3D as fitting a plane to a cloud of (x, y, z) points.


```python
data = pd.read_csv('data/iris.csv')
model = ols('sepal_width ~ name + petal_length', data).fit()
print(model.summary())  
```

                                OLS Regression Results                            
    ==============================================================================
    Dep. Variable:            sepal_width   R-squared:                       0.478
    Model:                            OLS   Adj. R-squared:                  0.468
    Method:                 Least Squares   F-statistic:                     44.63
    Date:                Thu, 21 Dec 2017   Prob (F-statistic):           1.58e-20
    Time:                        09:14:04   Log-Likelihood:                -38.185
    No. Observations:                 150   AIC:                             84.37
    Df Residuals:                     146   BIC:                             96.41
    Df Model:                           3                                         
    Covariance Type:            nonrobust                                         
    ======================================================================================
                             coef    std err          t      P>|t|      [95.0% Conf. Int.]
    --------------------------------------------------------------------------------------
    Intercept              2.9813      0.099     29.989      0.000         2.785     3.178
    name[T.versicolor]    -1.4821      0.181     -8.190      0.000        -1.840    -1.124
    name[T.virginica]     -1.6635      0.256     -6.502      0.000        -2.169    -1.158
    petal_length           0.2983      0.061      4.920      0.000         0.178     0.418
    ==============================================================================
    Omnibus:                        2.868   Durbin-Watson:                   1.753
    Prob(Omnibus):                  0.238   Jarque-Bera (JB):                2.885
    Skew:                          -0.082   Prob(JB):                        0.236
    Kurtosis:                       3.659   Cond. No.                         54.0
    ==============================================================================
    
    Warnings:
    [1] Standard Errors assume that the covariance matrix of the errors is correctly specified.
    

## Post-hoc hypothesis testing : ANOVA

In the above iris example, we wish **to test if the petal length is different between versicolor and virginica, after removing the effect of sepal width**. This can **be formulated as testing the difference between the coefficient associated to versicolor and virginica in the linear model estimated above** (it is an **Analysis of Variance, ANOVA**). For this, we write a vector of ‘contrast’ on the parameters estimated: we want to test "name[T.versicolor] - name[T.virginica]", with an F-test:



```python
print(model.f_test([0, 1, -1, 0]))  
```


```python
seaborn: 
    pairplot
    lmplot
    
```

## Testing for interactions

 


```python
result = sm.ols(formula='wage ~ education + gender + education * gender',
                data=data).fit()    
print(result.summary())   
```


