---
layout: post
title: OSMI mental health in tech survey data analysis
author: sara
categories: [Data Science]
image: assets/images/dogs/pexels-photo-357275.jpeg
featured: True
---
# Data Collection

The survey was distributed in 2016 by OSMI, a non-profit corporation providing support of metal wellness in the tech communities. Since it is an opt-in survey, people who are more interested in mental health are more likely to participate. Such resulting selection bias is worth noticing when making conclusions later.

# Data Cleaning

1. Assigning brief column names
2. Handling missing values
3. Fixing inconsistent data entry & spelling errors

## Column names

Data are quite clean while the column names are the exact questions on the questionaire which are not that convenient for analysis. So I'm here assigning brief ones in this step.


```python
%matplotlib inline

import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import re
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chisquare, chi2_contingency

import fuzzywuzzy
from fuzzywuzzy import process
import chardet

import os
raw = pd.read_csv("../input/mental-heath-in-tech-2016_20161114.csv")
pd.set_option('display.max_columns', raw.shape[1]+5)
```


```python
raw.shape
```




    (1433, 63)



We see that the survey data contains 1433 respondents with 63 variables.


```python
new_cols = ['self_employed',
 'num_employees',
 'tech_company',
 'tech_role',
 'mental_health_coverage',
 'mental_health_options',
 'mental_health_formally_discussed',
 'mental_health_resources',
 'anonymity_protected',
 'medical_leave',
 'mental_health_negative',
 'physical_health_negative',
 'mental_health_comfort_coworker',
 'mental_health_comfort_supervisor',
 'mental_health_taken_seriously',
 'coworker_negative_consequences',
 'private_med_coverage',
 'resources',
 'reveal_diagnosis_clients_or_business',
 'revealed_negative_consequences_CB',
 'reveal_diagnosis_coworkers',
 'revealed_negative_consequences_CW',
 'productivity_effected',
 'percentage',
 'previous_employer',
 'prevemp_mental_health_coverage',
 'prevemp_mental_health_options',
 'prevemp_mental_health_formally_discussed',
 'prevemp_mental_health_resources',
 'prevemp_anonymity_protected',
 'prevemp_mental_health_negative',
 'prevemp_physical_health_negative',
 'prevemp_mental_health_coworker',
 'prevemp_mental_health_comfort_supervisor',
 'prevemp_mental_health_taken_seriously',
 'prevemp_coworker_negative_consequences',
 'mention_phsyical_issue_interview',
 'why_whynot_physical',
 'mention_mental_health_interview',
 'why_whynot_mental',
 'career_hurt',
 'viewed_negatively_by_coworkers',
 'share_with_family',
 'observed_poor_handling',
 'observations_lead_less_likely_to_reveal',
 'family_history',
 'ever_had_mental_disorder',
 'currently_have_mental_disorder',
 'if_yes_what',
 'if_maybe_what',
 'medical_prof_diagnosis',
 'what_conditions',
 'sought_prof_treatment',
 'treatment_affects_work',
 'no_treatment_affects_work',
 'age',
 'gender',
 'country_live',
 'US_state',
 'country_work',
 'state_work',
 'work_position',
 'remotely']

raw.columns = new_cols
```

## Check missing values


```python
missed_var = raw.isnull().sum()
missed_var
```




    self_employed                                  0
    num_employees                                287
    tech_company                                 287
    tech_role                                   1170
    mental_health_coverage                       287
    mental_health_options                        420
    mental_health_formally_discussed             287
    mental_health_resources                      287
    anonymity_protected                          287
    medical_leave                                287
    mental_health_negative                       287
    physical_health_negative                     287
    mental_health_comfort_coworker               287
    mental_health_comfort_supervisor             287
    mental_health_taken_seriously                287
    coworker_negative_consequences               287
    private_med_coverage                        1146
    resources                                   1146
    reveal_diagnosis_clients_or_business        1146
    revealed_negative_consequences_CB           1289
    reveal_diagnosis_coworkers                  1146
    revealed_negative_consequences_CW           1146
    productivity_effected                       1146
    percentage                                  1229
    previous_employer                              0
    prevemp_mental_health_coverage               169
    prevemp_mental_health_options                169
    prevemp_mental_health_formally_discussed     169
    prevemp_mental_health_resources              169
    prevemp_anonymity_protected                  169
                                                ... 
    prevemp_mental_health_comfort_supervisor     169
    prevemp_mental_health_taken_seriously        169
    prevemp_coworker_negative_consequences       169
    mention_phsyical_issue_interview               0
    why_whynot_physical                          338
    mention_mental_health_interview                0
    why_whynot_mental                            307
    career_hurt                                    0
    viewed_negatively_by_coworkers                 0
    share_with_family                              0
    observed_poor_handling                        89
    observations_lead_less_likely_to_reveal      776
    family_history                                 0
    ever_had_mental_disorder                       0
    currently_have_mental_disorder                 0
    if_yes_what                                  865
    if_maybe_what                               1111
    medical_prof_diagnosis                         0
    what_conditions                              722
    sought_prof_treatment                          0
    treatment_affects_work                         0
    no_treatment_affects_work                      0
    age                                            0
    gender                                         3
    country_live                                   0
    US_state                                     593
    country_work                                   0
    state_work                                   582
    work_position                                  0
    remotely                                       0
    Length: 63, dtype: int64



There are values missing because they don't exist, like those for questions begin with 'If':
* If yes, what condition(s) have you been diagnosed with?
* If maybe, what condition(s) do you believe you have?
* If so, what condition(s) were you diagnosed with?
* ...

But why are there many repeated values? I guess some respondents finished surveys with many questions left empty. 


```python
missed_ppl = raw.isnull().sum(axis=1).sort_values(ascending=False)
raw.iloc[missed_ppl.index[missed_ppl>32]]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>self_employed</th>
      <th>num_employees</th>
      <th>tech_company</th>
      <th>tech_role</th>
      <th>mental_health_coverage</th>
      <th>mental_health_options</th>
      <th>mental_health_formally_discussed</th>
      <th>mental_health_resources</th>
      <th>anonymity_protected</th>
      <th>medical_leave</th>
      <th>mental_health_negative</th>
      <th>physical_health_negative</th>
      <th>mental_health_comfort_coworker</th>
      <th>mental_health_comfort_supervisor</th>
      <th>mental_health_taken_seriously</th>
      <th>coworker_negative_consequences</th>
      <th>private_med_coverage</th>
      <th>resources</th>
      <th>reveal_diagnosis_clients_or_business</th>
      <th>revealed_negative_consequences_CB</th>
      <th>reveal_diagnosis_coworkers</th>
      <th>revealed_negative_consequences_CW</th>
      <th>productivity_effected</th>
      <th>percentage</th>
      <th>previous_employer</th>
      <th>prevemp_mental_health_coverage</th>
      <th>prevemp_mental_health_options</th>
      <th>prevemp_mental_health_formally_discussed</th>
      <th>prevemp_mental_health_resources</th>
      <th>prevemp_anonymity_protected</th>
      <th>prevemp_mental_health_negative</th>
      <th>prevemp_physical_health_negative</th>
      <th>prevemp_mental_health_coworker</th>
      <th>prevemp_mental_health_comfort_supervisor</th>
      <th>prevemp_mental_health_taken_seriously</th>
      <th>prevemp_coworker_negative_consequences</th>
      <th>mention_phsyical_issue_interview</th>
      <th>why_whynot_physical</th>
      <th>mention_mental_health_interview</th>
      <th>why_whynot_mental</th>
      <th>career_hurt</th>
      <th>viewed_negatively_by_coworkers</th>
      <th>share_with_family</th>
      <th>observed_poor_handling</th>
      <th>observations_lead_less_likely_to_reveal</th>
      <th>family_history</th>
      <th>ever_had_mental_disorder</th>
      <th>currently_have_mental_disorder</th>
      <th>if_yes_what</th>
      <th>if_maybe_what</th>
      <th>medical_prof_diagnosis</th>
      <th>what_conditions</th>
      <th>sought_prof_treatment</th>
      <th>treatment_affects_work</th>
      <th>no_treatment_affects_work</th>
      <th>age</th>
      <th>gender</th>
      <th>country_live</th>
      <th>US_state</th>
      <th>country_work</th>
      <th>state_work</th>
      <th>work_position</th>
      <th>remotely</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>808</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>NaN</td>
      <td>No, I don't think it would</td>
      <td>Maybe</td>
      <td>Not applicable to me (I do not have a mental i...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>15</td>
      <td>male</td>
      <td>Canada</td>
      <td>NaN</td>
      <td>Canada</td>
      <td>NaN</td>
      <td>Other</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>877</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>I know some</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Yes</td>
      <td>26-50%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>No, I don't think they would</td>
      <td>Somewhat open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Rarely</td>
      <td>Sometimes</td>
      <td>50</td>
      <td>M</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>DevOps/SysAdmin</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>511</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>Maybe</td>
      <td>Not applicable to me (I do not have a mental i...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>I don't know</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>28</td>
      <td>male</td>
      <td>United States of America</td>
      <td>California</td>
      <td>United States of America</td>
      <td>California</td>
      <td>Other|Dev Evangelist/Advocate|One-person shop</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>1254</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>I'm not sure</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Yes</td>
      <td>26-50%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>Yes, I think it would</td>
      <td>Maybe</td>
      <td>Somewhat open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>45</td>
      <td>male</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>Back-end Developer|Front-end Developer|One-per...</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>563</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Yes</td>
      <td>1-25%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>not his concern</td>
      <td>No</td>
      <td>if he does his work correctly why should i</td>
      <td>No, I don't think it would</td>
      <td>No, they do not</td>
      <td>Somewhat open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>30</td>
      <td>male</td>
      <td>Poland</td>
      <td>NaN</td>
      <td>Poland</td>
      <td>NaN</td>
      <td>Supervisor/Team Lead|DevOps/SysAdmin|Back-end ...</td>
      <td>Always</td>
    </tr>
    <tr>
      <th>546</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Yes</td>
      <td>1-25%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Yes, I think it would</td>
      <td>Yes, I think they would</td>
      <td>Somewhat open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Anxiety Disorder (Generalized, Social, Phobia,...</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Anxiety Disorder (Generalized, Social, Phobia,...</td>
      <td>1</td>
      <td>Sometimes</td>
      <td>Sometimes</td>
      <td>30</td>
      <td>Male</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>Executive Leadership</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>811</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>I'm not sure</td>
      <td>Not applicable to me</td>
      <td>I'm not sure</td>
      <td>Yes</td>
      <td>26-50%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Yes, I think it would</td>
      <td>Maybe</td>
      <td>Neutral</td>
      <td>No</td>
      <td>NaN</td>
      <td>I don't know</td>
      <td>No</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Anxiety Disorder (Generalized, Social, Phobia,...</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Sometimes</td>
      <td>Sometimes</td>
      <td>27</td>
      <td>Male</td>
      <td>Romania</td>
      <td>NaN</td>
      <td>Romania</td>
      <td>NaN</td>
      <td>Support</td>
      <td>Always</td>
    </tr>
    <tr>
      <th>823</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>Yes, I know several</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Yes</td>
      <td>1-25%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>It depends on the situation. If it would imped...</td>
      <td>Maybe</td>
      <td>I deal with bouts of Anxiety and Depression bu...</td>
      <td>No, I don't think it would</td>
      <td>No, I don't think they would</td>
      <td>Somewhat open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>No</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Mood Disorder (Depression, Bipolar Disorder, e...</td>
      <td>No</td>
      <td>NaN</td>
      <td>1</td>
      <td>Rarely</td>
      <td>Sometimes</td>
      <td>35</td>
      <td>male</td>
      <td>Brunei</td>
      <td>NaN</td>
      <td>Brunei</td>
      <td>NaN</td>
      <td>One-person shop</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>1301</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>I know some</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>No</td>
      <td>Yes</td>
      <td>26-50%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>Maybe</td>
      <td>Not open at all</td>
      <td>Yes, I observed</td>
      <td>No</td>
      <td>Yes</td>
      <td>No</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Stress Response Syndromes|Post-traumatic Stres...</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Sometimes</td>
      <td>21</td>
      <td>Male</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>Executive Leadership|Supervisor/Team Lead|Dev ...</td>
      <td>Always</td>
    </tr>
    <tr>
      <th>1172</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>No, I don't know any</td>
      <td>No, because it doesn't matter</td>
      <td>NaN</td>
      <td>Sometimes, if it comes up</td>
      <td>No</td>
      <td>Yes</td>
      <td>76-100%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>No, I don't think it would</td>
      <td>No, I don't think they would</td>
      <td>Neutral</td>
      <td>No</td>
      <td>NaN</td>
      <td>No</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Psychotic Disorder (Schizophrenia, Schizoaffec...</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Psychotic Disorder (Schizophrenia, Schizoaffec...</td>
      <td>0</td>
      <td>Often</td>
      <td>Often</td>
      <td>35</td>
      <td>m</td>
      <td>Ireland</td>
      <td>NaN</td>
      <td>Ireland</td>
      <td>NaN</td>
      <td>Back-end Developer</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>450</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>Yes, I know several</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>It is by law none of the employer's business a...</td>
      <td>No</td>
      <td>For the same reasons as for physical health is...</td>
      <td>Yes, I think it would</td>
      <td>Maybe</td>
      <td>Somewhat open</td>
      <td>Yes, I observed</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>40</td>
      <td>Male</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>Germany</td>
      <td>NaN</td>
      <td>Executive Leadership</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>920</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>I know some</td>
      <td>Sometimes, if it comes up</td>
      <td>I'm not sure</td>
      <td>Sometimes, if it comes up</td>
      <td>I'm not sure</td>
      <td>Yes</td>
      <td>51-75%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>Maybe</td>
      <td>Very open</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>Obsessive-Compulsive Disorder</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>Obsessive-Compulsive Disorder</td>
      <td>1</td>
      <td>Often</td>
      <td>Often</td>
      <td>28</td>
      <td>Male</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>United Kingdom</td>
      <td>NaN</td>
      <td>Front-end Developer</td>
      <td>Always</td>
    </tr>
    <tr>
      <th>739</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0.0</td>
      <td>No, I don't know any</td>
      <td>Not applicable to me</td>
      <td>NaN</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>Unsure</td>
      <td>NaN</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>Sure</td>
      <td>Maybe</td>
      <td>Maybe</td>
      <td>Somewhat not open</td>
      <td>No</td>
      <td>NaN</td>
      <td>No</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>31</td>
      <td>Male</td>
      <td>United States of America</td>
      <td>Florida</td>
      <td>United States of America</td>
      <td>Florida</td>
      <td>Executive Leadership</td>
      <td>Sometimes</td>
    </tr>
    <tr>
      <th>113</th>
      <td>1</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1.0</td>
      <td>No, I don't know any</td>
      <td>No, because it doesn't matter</td>
      <td>I'm not sure</td>
      <td>Sometimes, if it comes up</td>
      <td>I'm not sure</td>
      <td>Yes</td>
      <td>76-100%</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Yes, it has</td>
      <td>Yes, I think they would</td>
      <td>Somewhat not open</td>
      <td>Yes, I observed</td>
      <td>No</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>NaN</td>
      <td>1</td>
      <td>Never</td>
      <td>Sometimes</td>
      <td>22</td>
      <td>Male</td>
      <td>Czech Republic</td>
      <td>NaN</td>
      <td>Czech Republic</td>
      <td>NaN</td>
      <td>Back-end Developer|Front-end Developer</td>
      <td>Sometimes</td>
    </tr>
  </tbody>
</table>
</div>



I see. There are questions that self-employed respondants don't need to answer. 

It reminds me that self-employment is a quite different style of work when compared to those with monthly salary. I will divide them into 2 groups for analysis related to employer or colleagues.



## Fixing inconsistent data entry & spelling errors

Free-form surveys always bring us a little headache with inconsistent data entry and spelling errors. I will do a Fuzzy matching and correct the rest by hand. 

> __Fuzzy matching__ is a process of automatically finding text strings that are very similar to the target string. In general, a string is considered "closer" to another one the fewer characters you'd need to change if you were transforming one string into another.



```python
def fuzzy_match(df, column, to_matches, min_ratio = 85):
    strings = df[column].unique()
    for to_match in to_matches:
        matches = fuzzywuzzy.process.extract(to_match, strings,
                                            limit=10,scorer=fuzzywuzzy.fuzz.token_sort_ratio)
        close_matches = [matches[0] for matches in matches if matches[1] >= min_ratio]
        rows_matched = df[column].isin(close_matches)
        df.loc[rows_matched, column] = to_match
        print("Matches of {} on column {} done!".format(to_match, column))
```


```python
fuzzy_match(raw, 'gender',['female','woman','male','man'])
# raw['gender'].fillna('None',inplace=True)
# raw[raw.gender.str.contains('f')]['gender'] = 'female'
raw['gender'] = raw['gender'].replace(['woman','F','fm','f','Cis-woman',
                                       'Cis female'],'female')
raw['gender'] = raw['gender'].replace(['M','m','Male (cis)','cis man',
                                      ],'male')
raw[~(raw['gender'].isin(['female','male']))] = 'others'
```

    Matches of female on column gender done!
    Matches of woman on column gender done!
    Matches of male on column gender done!
    Matches of man on column gender done!


# Exploratory Data Analysis

My goal is to find variables potentially correlate to the incidence of mental health condition.

```python
raw['currently_have_mental_disorder'].value_counts().sort_index().plot.bar()
plt.title("Do you currently have a mental health disorder?")
plt.show()
raw['ever_had_mental_disorder'].value_counts().sort_index().plot.bar()
plt.title("Have you had a mental health disorder in the past?")
plt.show()
raw['medical_prof_diagnosis'].value_counts().sort_index().plot.bar()
plt.title("Have you been diagnosed with a mental health condition by a medical professional?")
plt.show()

```


![png](/assets/images/osmi/output_14_0.png)



![png](/assets/images/osmi/output_14_1.png)



![png](/assets/images/osmi/output_14_2.png)


50% of our respondents have been diagnosed with a mental health condition by a medical professional. Remember the selection bias I mentioned on the Data Collection part? The actual incidence rate should be lower. I still hold a positive perspective that there are larger proportion of developers out there having a strong mind like I do ;)

But more than half are believed to be suffering or have been suffered from mental disorder. Why is that?

I guess they do not seek for help when suffering. Let me have a check if data agree with me. 

###  what condition(s) were you diagnosed with?

There are 116 different responses on this question. I did some recoding based on domain knowledge and created binary variables for each mental health disorder diagnosed for later use. Since there are respondents diagnosed with multiple mental health conditions, the figure below is not a distribution plot in a traditional sense. 



```python
disorder = {}
disorder_count = dict(raw['what_conditions'].value_counts())
for k,v in disorder_count.items():
    ks = k.split("|")
    for j in ks:
        j = j.split(' (')[0]
        disorder[j] = disorder.get(j,0)+v
```


```python
raw['what_conditions'].fillna('None',inplace=True)
raw['condition_list'] = raw.what_conditions.map(lambda x: [j.split(' (')[0] for j in x.split("|")])
```


```python
disorders = {
    'Autism':['Autism Spectrum Disorder', 'Autism - while not a "mental illness", still greatly affects how I handle anxiety',
    'autism spectrum disorder', 'PDD-NOS'],
    "Asperger's Syndrome":['Aspergers', 'Asperger Syndrome'],
    "Post-traumatic Stress Disorder":['posttraumatic stress disourder'],
    "Attention Deficit Hyperactivity Disorder":['ADD', 'Attention Deficit Disorder', 'attention deficit disorder'],
    "Personality Disorder":['Schizotypal Personality Disorder'],
    "Mood Disorder":["Depression"],
    "Others":['Autism', "Asperger's Syndrome", 'Intimate Disorder',
    'Seasonal Affective Disorder', 'Burn out', 'Gender Identity Disorder',
    'Suicidal Ideation', 'Gender Dysphoria', 'MCD']
}
```


```python
for k, v in disorders.items():
    raw['is_{}'.format(k)] = raw.condition_list.map(lambda x: bool(set(x).intersection(v+[k])))
```


```python
tmp = pd.DataFrame()
for i in disorder:
    tmp = tmp.append([i] * disorder[i])

for k,v in disorder.items():
    tmp[0] = tmp[0].replace(v,k)

# print(tmp[0].value_counts())
g = sns.countplot(y=tmp[0], order=[
    'Mood Disorder', 'Anxiety Disorder', 'Attention Deficit Hyperactivity Disorder',
    'Post-traumatic Stress Disorder', 'Obsessive-Compulsive Disorder',
    'Stress Response Syndromes', 'Personality Disorder', 'Substance Use Disorder',
    'Eating Disorder', 'Addictive Disorder', 'Dissociative Disorder', 
    'Psychotic Disorder', 'Others'])
g.set_ylabel('Disorders')
g.set_title('Distribution of Mental Health Disorders')
plt.show()
```


![png](/assets/images/osmi/output_21_0.png)



```python
g = sns.countplot(x = 'num_employees',
                 hue = 'mental_health_coverage',
                 data = raw,
                 order = ['1-5','5-25','26-100','100-500','500-1000','More than 1000'],
                 hue_order = ['Yes', 'No', "I don't know","Not eligible for coverage / N/A"])

plt.legend(bbox_to_anchor=(1.05,1),loc=2,borderaxespad=0)
plt.figure(figsize=(6,12))
plt.show()
```


![png](/assets/images/osmi/output_22_0.png)



    <matplotlib.figure.Figure at 0x7f0f63050588>



```python
raw['mental_health_taken_seriously'].unique()
```




    array(["I don't know", 'Yes', nan, 'No', 'others'], dtype=object)




```python
contigenctTable = pd.crosstab(raw['num_employees'],raw['mental_health_taken_seriously'])
chi2_contingency(contigenctTable)
```




    (1188.7279580158292,
     2.9092304930171702e-241,
     18,
     array([[ 23.35177182,  13.94209162,  16.75021608,   2.95592048],
            [ 97.91356958,  58.45894555,  70.23336214,  12.39412273],
            [115.9394987 ,  69.22126188,  83.1633535 ,  14.67588591],
            [ 31.13569576,  18.58945549,  22.33362143,   3.94122731],
            [ 81.93604149,  48.91961971,  58.77268799,  10.37165082],
            [ 99.1426102 ,  59.19273984,  71.11495246,  12.54969749],
            [ 24.58081245,  14.67588591,  17.6318064 ,   3.11149525]]))




```python
contigenctTable2 = pd.crosstab(raw['num_employees'],raw['mental_health_formally_discussed'])
chi2_contingency(contigenctTable2)
```




    (1223.1151725675513,
     1.2462420185184758e-248,
     18,
     array([[  4.97579948,  38.32843561,  10.73984443,   2.95592048],
            [ 20.86343993, 160.71045808,  45.03197926,  12.39412273],
            [ 24.70440795, 190.29732066,  53.32238548,  14.67588591],
            [  6.63439931,  51.10458081,  14.31979257,   3.94122731],
            [ 17.45894555, 134.48573898,  37.68366465,  10.37165082],
            [ 21.12532411, 162.72774417,  45.59723423,  12.54969749],
            [  5.23768366,  40.34572169,  11.30509939,   3.11149525]]))



## Outlier



    34.34814275309541




```python
ages = [a for a in raw['age'] if isinstance(a, int)]
m = np.mean(ages)
sd = np.std(ages)
outliers = [a for a in ages if (a> m+2*sd) or (a<m-2*sd)]
outliers
```




    [57,
     63,
     57,
     61,
     61,
     323,
     62,
     58,
     3,
     66,
     59,
     63,
     59,
     65,
     63,
     74,
     57,
     57,
     70,
     63]




```python
pos_dict = {}
pos_count = dict(raw['work_position'].value_counts())
for k,v in pos_count.items():
    ks = k.split("|")
    for j in ks:
        pos_dict[j] = pos_dict.get(j,0)+v

pos_dict
```




    {'Back-end Developer': 702,
     'Designer': 126,
     'Dev Evangelist/Advocate': 94,
     'DevOps/SysAdmin': 267,
     'Executive Leadership': 98,
     'Front-end Developer': 477,
     'HR': 10,
     'One-person shop': 154,
     'Other': 171,
     'Sales': 29,
     'Supervisor/Team Lead': 266,
     'Support': 156,
     'others': 60}




```python
posdf = pd.DataFrame()
posdf['currently_have_mental_disorder'] = raw.currently_have_mental_disorder.map(lambda x: x != 'No')
# posdf['num_po'] = raw.work_position.map(lambda x: x.find("|")+1)
for k, v in pos_dict.items():
    posdf['is_{}'.format(k)] = raw.work_position.map(lambda x: k in x)
```


```python
corr = posdf.corr()
mask = np.zeros_like(corr, dtype=np.bool)
mask[np.triu_indices_from(mask)] = True
# Generate a custom diverging colormap
cmap = sns.diverging_palette(220, 10, as_cmap=True)
sns.heatmap(corr, mask=mask, cmap=cmap,annot=True)
```




    <matplotlib.axes._subplots.AxesSubplot at 0x7f0fbba8cf98>




![png](/assets/images/osmi/output_31_1.png)



```python
raw['country_work'].value_counts()
```




    United States of America    818
    United Kingdom              173
    Canada                       69
    others                       60
    Germany                      55
    Netherlands                  44
    Australia                    34
    Sweden                       17
    Ireland                      14
    France                       13
    Brazil                       10
    India                         9
    Russia                        9
    New Zealand                   9
    Switzerland                   9
    Bulgaria                      7
    Finland                       7
    Denmark                       7
    Belgium                       5
    Poland                        4
    Austria                       4
    South Africa                  4
    Italy                         3
    Romania                       3
    Norway                        3
    Spain                         3
    Chile                         3
    Czech Republic                3
    Estonia                       2
    Other                         2
    Bosnia and Herzegovina        2
    Afghanistan                   2
    Pakistan                      2
    Colombia                      2
    Mexico                        2
    Israel                        2
    United Arab Emirates          1
    Vietnam                       1
    Slovakia                      1
    Guatemala                     1
    Japan                         1
    Brunei                        1
    Costa Rica                    1
    Ecuador                       1
    Venezuela                     1
    Greece                        1
    Serbia                        1
    Iran                          1
    Bangladesh                    1
    Turkey                        1
    China                         1
    Hungary                       1
    Argentina                     1
    Lithuania                     1
    Name: country_work, dtype: int64



Over half of our respondents come from the United States. Other frequently appeared countries include developed coutries like United Kindom, Canada and Germany etc., which suggests that our samples are not offering a picture of the stress culture that might exist in emerging markets like China.


```python
# geo related
# country_live	US_state	country_work	state_work
raw['US_state'] = raw['US_state'].fillna(raw['country_live'])
raw['state_work'] = raw['state_work'].fillna(raw['country_work'])

```


```python
raw[raw['age'].isin([3,99,323])]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>self_employed</th>
      <th>num_employees</th>
      <th>tech_company</th>
      <th>tech_role</th>
      <th>mental_health_coverage</th>
      <th>mental_health_options</th>
      <th>mental_health_formally_discussed</th>
      <th>mental_health_resources</th>
      <th>anonymity_protected</th>
      <th>medical_leave</th>
      <th>mental_health_negative</th>
      <th>physical_health_negative</th>
      <th>mental_health_comfort_coworker</th>
      <th>mental_health_comfort_supervisor</th>
      <th>mental_health_taken_seriously</th>
      <th>coworker_negative_consequences</th>
      <th>private_med_coverage</th>
      <th>resources</th>
      <th>reveal_diagnosis_clients_or_business</th>
      <th>revealed_negative_consequences_CB</th>
      <th>reveal_diagnosis_coworkers</th>
      <th>revealed_negative_consequences_CW</th>
      <th>productivity_effected</th>
      <th>percentage</th>
      <th>previous_employer</th>
      <th>prevemp_mental_health_coverage</th>
      <th>prevemp_mental_health_options</th>
      <th>prevemp_mental_health_formally_discussed</th>
      <th>prevemp_mental_health_resources</th>
      <th>prevemp_anonymity_protected</th>
      <th>prevemp_mental_health_negative</th>
      <th>prevemp_physical_health_negative</th>
      <th>prevemp_mental_health_coworker</th>
      <th>prevemp_mental_health_comfort_supervisor</th>
      <th>...</th>
      <th>why_whynot_physical</th>
      <th>mention_mental_health_interview</th>
      <th>why_whynot_mental</th>
      <th>career_hurt</th>
      <th>viewed_negatively_by_coworkers</th>
      <th>share_with_family</th>
      <th>observed_poor_handling</th>
      <th>observations_lead_less_likely_to_reveal</th>
      <th>family_history</th>
      <th>ever_had_mental_disorder</th>
      <th>currently_have_mental_disorder</th>
      <th>if_yes_what</th>
      <th>if_maybe_what</th>
      <th>medical_prof_diagnosis</th>
      <th>what_conditions</th>
      <th>sought_prof_treatment</th>
      <th>treatment_affects_work</th>
      <th>no_treatment_affects_work</th>
      <th>age</th>
      <th>gender</th>
      <th>country_live</th>
      <th>US_state</th>
      <th>country_work</th>
      <th>state_work</th>
      <th>work_position</th>
      <th>remotely</th>
      <th>condition_list</th>
      <th>is_Autism</th>
      <th>is_Asperger's Syndrome</th>
      <th>is_Post-traumatic Stress Disorder</th>
      <th>is_Attention Deficit Hyperactivity Disorder</th>
      <th>is_Personality Disorder</th>
      <th>is_Mood Disorder</th>
      <th>is_Others</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>564</th>
      <td>0</td>
      <td>100-500</td>
      <td>1</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>No</td>
      <td>I don't know</td>
      <td>I don't know</td>
      <td>I don't know</td>
      <td>I don't know</td>
      <td>No</td>
      <td>No</td>
      <td>Maybe</td>
      <td>Maybe</td>
      <td>I don't know</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>Some did</td>
      <td>N/A (not currently aware)</td>
      <td>None did</td>
      <td>None did</td>
      <td>I don't know</td>
      <td>I don't know</td>
      <td>Some of them</td>
      <td>Some of my previous employers</td>
      <td>Some of my previous employers</td>
      <td>...</td>
      <td>It may affect time I need to take off or my ab...</td>
      <td>Maybe</td>
      <td>It hasn't come up for me.</td>
      <td>Maybe</td>
      <td>No, I don't think they would</td>
      <td>Neutral</td>
      <td>Maybe/Not sure</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>No</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>No</td>
      <td>None</td>
      <td>0</td>
      <td>Not applicable to me</td>
      <td>Not applicable to me</td>
      <td>323</td>
      <td>male</td>
      <td>United States of America</td>
      <td>Oregon</td>
      <td>United States of America</td>
      <td>Oregon</td>
      <td>Back-end Developer</td>
      <td>Sometimes</td>
      <td>[None]</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
    <tr>
      <th>656</th>
      <td>0</td>
      <td>More than 1000</td>
      <td>1</td>
      <td>NaN</td>
      <td>Yes</td>
      <td>I am not sure</td>
      <td>Yes</td>
      <td>Yes</td>
      <td>I don't know</td>
      <td>Somewhat easy</td>
      <td>Maybe</td>
      <td>No</td>
      <td>Maybe</td>
      <td>Yes</td>
      <td>I don't know</td>
      <td>No</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>1</td>
      <td>Some did</td>
      <td>I was aware of some</td>
      <td>None did</td>
      <td>Some did</td>
      <td>I don't know</td>
      <td>Some of them</td>
      <td>Some of them</td>
      <td>No, at none of my previous employers</td>
      <td>Some of my previous employers</td>
      <td>...</td>
      <td>Legislation in my jurisdiction mandates certai...</td>
      <td>No</td>
      <td>Despite the legal protections, mental health i...</td>
      <td>Maybe</td>
      <td>No, I don't think they would</td>
      <td>Somewhat open</td>
      <td>Maybe/Not sure</td>
      <td>Maybe</td>
      <td>I don't know</td>
      <td>Yes</td>
      <td>Maybe</td>
      <td>NaN</td>
      <td>Anxiety Disorder (Generalized, Social, Phobia,...</td>
      <td>Yes</td>
      <td>Anxiety Disorder (Generalized, Social, Phobia,...</td>
      <td>1</td>
      <td>Rarely</td>
      <td>Sometimes</td>
      <td>3</td>
      <td>male</td>
      <td>Canada</td>
      <td>Canada</td>
      <td>Canada</td>
      <td>Canada</td>
      <td>Back-end Developer</td>
      <td>Sometimes</td>
      <td>[Anxiety Disorder]</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
      <td>False</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 71 columns</p>
</div>
