---
layout: post
title: From Exploratory Analysis to Feature Engineering
author: sara
categories: [Data Science]
image: assets/images/dogs/pexels-photo-179107.jpeg
featured: False
---

Following can be considered as a routinue for me every time I start doing exploratory analysis for a new machine learning project:
1. What is the problem I'm going to solve?
2. Know more about dependent variable ('SalePrice' in this case)
3. What data can I get as independent variabls and how are they related?


```python
import pandas as pd
import matplotlib.pyplot as plt
from ggplot import *
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler, LabelEncoder
import numpy as np
from scipy.stats import skew

```


```python
train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')
```


```python
train.sample(5)
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
      <th>Id</th>
      <th>MSSubClass</th>
      <th>MSZoning</th>
      <th>LotFrontage</th>
      <th>LotArea</th>
      <th>Street</th>
      <th>Alley</th>
      <th>LotShape</th>
      <th>LandContour</th>
      <th>Utilities</th>
      <th>...</th>
      <th>PoolArea</th>
      <th>PoolQC</th>
      <th>Fence</th>
      <th>MiscFeature</th>
      <th>MiscVal</th>
      <th>MoSold</th>
      <th>YrSold</th>
      <th>SaleType</th>
      <th>SaleCondition</th>
      <th>SalePrice</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1121</th>
      <td>1122</td>
      <td>20</td>
      <td>RL</td>
      <td>84.0</td>
      <td>10084</td>
      <td>Pave</td>
      <td>NaN</td>
      <td>Reg</td>
      <td>Lvl</td>
      <td>AllPub</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>7</td>
      <td>2006</td>
      <td>New</td>
      <td>Partial</td>
      <td>212900</td>
    </tr>
    <tr>
      <th>26</th>
      <td>27</td>
      <td>20</td>
      <td>RL</td>
      <td>60.0</td>
      <td>7200</td>
      <td>Pave</td>
      <td>NaN</td>
      <td>Reg</td>
      <td>Lvl</td>
      <td>AllPub</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>5</td>
      <td>2010</td>
      <td>WD</td>
      <td>Normal</td>
      <td>134800</td>
    </tr>
    <tr>
      <th>592</th>
      <td>593</td>
      <td>20</td>
      <td>RL</td>
      <td>60.0</td>
      <td>6600</td>
      <td>Pave</td>
      <td>NaN</td>
      <td>Reg</td>
      <td>Lvl</td>
      <td>AllPub</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>6</td>
      <td>2008</td>
      <td>WD</td>
      <td>Normal</td>
      <td>138000</td>
    </tr>
    <tr>
      <th>886</th>
      <td>887</td>
      <td>90</td>
      <td>RL</td>
      <td>70.0</td>
      <td>8393</td>
      <td>Pave</td>
      <td>NaN</td>
      <td>Reg</td>
      <td>Lvl</td>
      <td>AllPub</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>6</td>
      <td>2006</td>
      <td>WD</td>
      <td>Family</td>
      <td>145000</td>
    </tr>
    <tr>
      <th>275</th>
      <td>276</td>
      <td>50</td>
      <td>RL</td>
      <td>55.0</td>
      <td>7264</td>
      <td>Pave</td>
      <td>NaN</td>
      <td>Reg</td>
      <td>Lvl</td>
      <td>AllPub</td>
      <td>...</td>
      <td>0</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>0</td>
      <td>10</td>
      <td>2009</td>
      <td>WD</td>
      <td>Normal</td>
      <td>205000</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 81 columns</p>
</div>




```python
train.drop(train[(train["GrLivArea"]>4000)&(train["SalePrice"]<300000)].index,inplace=True)
```


```python
y_raw = train['SalePrice']
all_data = pd.concat([train, test],ignore_index=True)
all_data.drop(['Id','SalePrice'],axis=1,inplace=True)
all_cat = all_data.select_dtypes(include=["object"])
all_num = all_data.select_dtypes(exclude=["object"])

print("Categorical variables: \n{}".format("\n".join(all_cat.columns)))
```

    Categorical variables: 
    Alley
    BldgType
    BsmtCond
    BsmtExposure
    BsmtFinType1
    BsmtFinType2
    BsmtQual
    CentralAir
    Condition1
    Condition2
    Electrical
    ExterCond
    ExterQual
    Exterior1st
    Exterior2nd
    Fence
    FireplaceQu
    Foundation
    Functional
    GarageCond
    GarageFinish
    GarageQual
    GarageType
    Heating
    HeatingQC
    HouseStyle
    KitchenQual
    LandContour
    LandSlope
    LotConfig
    LotShape
    MSZoning
    MasVnrType
    MiscFeature
    Neighborhood
    PavedDrive
    PoolQC
    RoofMatl
    RoofStyle
    SaleCondition
    SaleType
    Street
    Utilities



```python
print("Numerical variables: \n{}".format("\n".join(all_num.columns)))
```

    Numerical variables: 
    1stFlrSF
    2ndFlrSF
    3SsnPorch
    BedroomAbvGr
    BsmtFinSF1
    BsmtFinSF2
    BsmtFullBath
    BsmtHalfBath
    BsmtUnfSF
    EnclosedPorch
    Fireplaces
    FullBath
    GarageArea
    GarageCars
    GarageYrBlt
    GrLivArea
    HalfBath
    KitchenAbvGr
    LotArea
    LotFrontage
    LowQualFinSF
    MSSubClass
    MasVnrArea
    MiscVal
    MoSold
    OpenPorchSF
    OverallCond
    OverallQual
    PoolArea
    ScreenPorch
    TotRmsAbvGrd
    TotalBsmtSF
    WoodDeckSF
    YearBuilt
    YearRemodAdd
    YrSold



```python
missed = all_data.isnull().sum()
missed[missed>0].sort_values(ascending=False)
```




    PoolQC          2908
    MiscFeature     2812
    Alley           2719
    Fence           2346
    FireplaceQu     1420
    LotFrontage      486
    GarageQual       159
    GarageCond       159
    GarageFinish     159
    GarageYrBlt      159
    GarageType       157
    BsmtExposure      82
    BsmtCond          82
    BsmtQual          81
    BsmtFinType2      80
    BsmtFinType1      79
    MasVnrType        24
    MasVnrArea        23
    MSZoning           4
    BsmtFullBath       2
    BsmtHalfBath       2
    Utilities          2
    Functional         2
    Electrical         1
    BsmtUnfSF          1
    Exterior1st        1
    Exterior2nd        1
    TotalBsmtSF        1
    GarageArea         1
    GarageCars         1
    BsmtFinSF2         1
    BsmtFinSF1         1
    KitchenQual        1
    SaleType           1
    dtype: int64



There are many missing values in 'PoolQC', let's have a check if it is related to 'PoolArea'


```python
all_data['PoolArea'].describe()
```




    count    2917.000000
    mean        2.088790
    std        34.561371
    min         0.000000
    25%         0.000000
    50%         0.000000
    75%         0.000000
    max       800.000000
    Name: PoolArea, dtype: float64




```python
all_data[all_data['PoolArea']==0]['PoolQC'].isnull().sum()
```




    2905




```python
all_data.loc[(all_data['PoolArea']!=0) & (all_data['PoolQC'].isnull()),['PoolArea']]
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
      <th>PoolArea</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2418</th>
      <td>368</td>
    </tr>
    <tr>
      <th>2501</th>
      <td>444</td>
    </tr>
    <tr>
      <th>2597</th>
      <td>561</td>
    </tr>
  </tbody>
</table>
</div>




```python
all_data['PoolQC'].value_counts()
```




    Ex    4
    Gd    3
    Fa    2
    Name: PoolQC, dtype: int64



Seems that most of the missing values in 'PoolQC' come from houses without a pool. Let's fill in the missing values here.


```python
all_data.loc[(all_data['PoolArea']==0) & (all_data['PoolQC'].isnull()),['PoolQC']]='NA'
```

Missing values in 'LotFrontage' can be imputed based on LotArea and Neighborhood


```python
all_data["LotAreaCut"] = pd.qcut(all_data.LotArea,10)
all_data['LotFrontage']=all_data.groupby(['LotAreaCut','Neighborhood'])['LotFrontage'].transform(lambda x: x.fillna(x.median()))
all_data['LotFrontage'].isnull().sum()

```




    9



For those with missing values in either LotArea or Neighborhood, we use LotAreaCut only.


```python
all_data['LotFrontage']=all_data.groupby(['LotAreaCut'])['LotFrontage'].transform(lambda x: x.fillna(x.median()))
```


```python
all_data['LotFrontage'].isnull().sum()
```




    0




```python
for col in missed[missed<20].index:
    all_data[col].fillna(all_data[col].mode()[0],inplace=True)
```


```python
for col in all_num.columns:
    all_data[col].fillna(0,inplace=True)
```


```python
for col in all_cat.columns:
    all_data[col].fillna("None",inplace=True)
```


```python
sum(all_data.isnull().sum()>0)
```




    0




```python
NumStr = ["MSSubClass","BsmtFullBath","BsmtHalfBath","HalfBath","BedroomAbvGr","KitchenAbvGr","MoSold","YrSold","YearBuilt","YearRemodAdd","LowQualFinSF","GarageYrBlt"]
for col in NumStr:
    all_data[col]=all_data[col].astype(str)

def map_values():
    all_data["oMSSubClass"] = all_data.MSSubClass.map({'180':1, 
                                        '30':2, '45':2, 
                                        '190':3, '50':3, '90':3, 
                                        '85':4, '40':4, '160':4, 
                                        '70':5, '20':5, '75':5, '80':5, '150':5,
                                        '120': 6, '60':6})
    
    all_data["oMSZoning"] = all_data.MSZoning.map({'C (all)':1, 'RH':2, 'RM':2, 'RL':3, 'FV':4})
    
    all_data["oNeighborhood"] = all_data.Neighborhood.map({'MeadowV':1,
                                               'IDOTRR':2, 'BrDale':2,
                                               'OldTown':3, 'Edwards':3, 'BrkSide':3,
                                               'Sawyer':4, 'Blueste':4, 'SWISU':4, 'NAmes':4,
                                               'NPkVill':5, 'Mitchel':5,
                                               'SawyerW':6, 'Gilbert':6, 'NWAmes':6,
                                               'Blmngtn':7, 'CollgCr':7, 'ClearCr':7, 'Crawfor':7,
                                               'Veenker':8, 'Somerst':8, 'Timber':8,
                                               'StoneBr':9,
                                               'NoRidge':10, 'NridgHt':10})
    
    all_data["oCondition1"] = all_data.Condition1.map({'Artery':1,
                                           'Feedr':2, 'RRAe':2,
                                           'Norm':3, 'RRAn':3,
                                           'PosN':4, 'RRNe':4,
                                           'PosA':5 ,'RRNn':5})
    
    all_data["oBldgType"] = all_data.BldgType.map({'2fmCon':1, 'Duplex':1, 'Twnhs':1, '1Fam':2, 'TwnhsE':2})
    
    all_data["oHouseStyle"] = all_data.HouseStyle.map({'1.5Unf':1, 
                                           '1.5Fin':2, '2.5Unf':2, 'SFoyer':2, 
                                           '1Story':3, 'SLvl':3,
                                           '2Story':4, '2.5Fin':4})
    
    all_data["oExterior1st"] = all_data.Exterior1st.map({'BrkComm':1,
                                             'AsphShn':2, 'CBlock':2, 'AsbShng':2,
                                             'WdShing':3, 'Wd Sdng':3, 'MetalSd':3, 'Stucco':3, 'HdBoard':3,
                                             'BrkFace':4, 'Plywood':4,
                                             'VinylSd':5,
                                             'CemntBd':6,
                                             'Stone':7, 'ImStucc':7})
    
    all_data["oMasVnrType"] = all_data.MasVnrType.map({'BrkCmn':1, 'None':1, 'BrkFace':2, 'Stone':3})
    
    all_data["oExterQual"] = all_data.ExterQual.map({'Fa':1, 'TA':2, 'Gd':3, 'Ex':4})
    
    all_data["oFoundation"] = all_data.Foundation.map({'Slab':1, 
                                           'BrkTil':2, 'CBlock':2, 'Stone':2,
                                           'Wood':3, 'PConc':4})
    
    all_data["oBsmtQual"] = all_data.BsmtQual.map({'Fa':2, 'None':1, 'TA':3, 'Gd':4, 'Ex':5})
    
    all_data["oBsmtExposure"] = all_data.BsmtExposure.map({'None':1, 'No':2, 'Av':3, 'Mn':3, 'Gd':4})
    
    all_data["oHeating"] = all_data.Heating.map({'Floor':1, 'Grav':1, 'Wall':2, 'OthW':3, 'GasW':4, 'GasA':5})
    
    all_data["oHeatingQC"] = all_data.HeatingQC.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
    
    all_data["oKitchenQual"] = all_data.KitchenQual.map({'Fa':1, 'TA':2, 'Gd':3, 'Ex':4})
    
    all_data["oFunctional"] = all_data.Functional.map({'Maj2':1, 'Maj1':2, 'Min1':2, 'Min2':2, 'Mod':2, 'Sev':2, 'Typ':3})
    
    all_data["oFireplaceQu"] = all_data.FireplaceQu.map({'None':1, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
    
    all_data["oGarageType"] = all_data.GarageType.map({'CarPort':1, 'None':1,
                                           'Detchd':2,
                                           '2Types':3, 'Basment':3,
                                           'Attchd':4, 'BuiltIn':5})
    
    all_data["oGarageFinish"] = all_data.GarageFinish.map({'None':1, 'Unf':2, 'RFn':3, 'Fin':4})
    
    all_data["oPavedDrive"] = all_data.PavedDrive.map({'N':1, 'P':2, 'Y':3})
    
    all_data["oSaleType"] = all_data.SaleType.map({'COD':1, 'ConLD':1, 'ConLI':1, 'ConLw':1, 'Oth':1, 'WD':1,
                                       'CWD':2, 'Con':3, 'New':3})
    
    all_data["oSaleCondition"] = all_data.SaleCondition.map({'AdjLand':1, 'Abnorml':2, 'Alloca':2, 'Family':2, 'Normal':3, 'Partial':4})            
                
                        
                        
    
    return "Done!"

map_values()


```




    'Done!'




```python
all_data.drop("LotAreaCut",axis=1,inplace=True)


```


```python
#all_data.drop(['SalePrice'],axis=1,inplace=True)

class labelenc(BaseEstimator, TransformerMixin):
    def __init__(self):
        pass
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        lab=LabelEncoder()
        X["YearBuilt"] = lab.fit_transform(X["YearBuilt"])
        X["YearRemodAdd"] = lab.fit_transform(X["YearRemodAdd"])
        X["GarageYrBlt"] = lab.fit_transform(X["GarageYrBlt"])
        return X
    
class skew_dummies(BaseEstimator, TransformerMixin):
    def __init__(self,skew=0.5):
        self.skew = skew
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        X_numeric=X.select_dtypes(exclude=["object"])
        skewness = X_numeric.apply(lambda x: skew(x))
        skewness_features = skewness[abs(skewness) >= self.skew].index
        X[skewness_features] = np.log1p(X[skewness_features])
        X = pd.get_dummies(X)
        return X
    
pipe = Pipeline([
    ('labenc', labelenc()),
    ('skew_dummies', skew_dummies(skew=1)),
    ])

all_data2 = all_data.copy()

data_pipe = pipe.fit_transform(all_data2)

scaler = RobustScaler()

n_train=train.shape[0]

X = data_pipe[:n_train]
test_X = data_pipe[n_train:]
y= train.SalePrice

X_scaled = scaler.fit(X).transform(X)
y_log = np.log(train.SalePrice)
test_X_scaled = scaler.transform(test_X)
```


```python
class add_feature(BaseEstimator, TransformerMixin):
    def __init__(self,additional=1):
        self.additional = additional
    
    def fit(self,X,y=None):
        return self
    
    def transform(self,X):
        if self.additional==1:
            X["TotalHouse"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"]   
            X["TotalArea"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"] + X["GarageArea"]
            
        else:
            X["TotalHouse"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"]   
            X["TotalArea"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"] + X["GarageArea"]
            
            X["+_TotalHouse_OverallQual"] = X["TotalHouse"] * X["OverallQual"]
            X["+_GrLivArea_OverallQual"] = X["GrLivArea"] * X["OverallQual"]
            X["+_oMSZoning_TotalHouse"] = X["oMSZoning"] * X["TotalHouse"]
            X["+_oMSZoning_OverallQual"] = X["oMSZoning"] + X["OverallQual"]
            X["+_oMSZoning_YearBuilt"] = X["oMSZoning"] + X["YearBuilt"]
            X["+_oNeighborhood_TotalHouse"] = X["oNeighborhood"] * X["TotalHouse"]
            X["+_oNeighborhood_OverallQual"] = X["oNeighborhood"] + X["OverallQual"]
            X["+_oNeighborhood_YearBuilt"] = X["oNeighborhood"] + X["YearBuilt"]
            X["+_BsmtFinSF1_OverallQual"] = X["BsmtFinSF1"] * X["OverallQual"]
            
            X["-_oFunctional_TotalHouse"] = X["oFunctional"] * X["TotalHouse"]
            X["-_oFunctional_OverallQual"] = X["oFunctional"] + X["OverallQual"]
            X["-_LotArea_OverallQual"] = X["LotArea"] * X["OverallQual"]
            X["-_TotalHouse_LotArea"] = X["TotalHouse"] + X["LotArea"]
            X["-_oCondition1_TotalHouse"] = X["oCondition1"] * X["TotalHouse"]
            X["-_oCondition1_OverallQual"] = X["oCondition1"] + X["OverallQual"]
            
           
            X["Bsmt"] = X["BsmtFinSF1"] + X["BsmtFinSF2"] + X["BsmtUnfSF"]
            X["Rooms"] = X["FullBath"]+X["TotRmsAbvGrd"]
            X["PorchArea"] = X["OpenPorchSF"]+X["EnclosedPorch"]+X["3SsnPorch"]+X["ScreenPorch"]
            X["TotalPlace"] = X["TotalBsmtSF"] + X["1stFlrSF"] + X["2ndFlrSF"] + X["GarageArea"] + X["OpenPorchSF"]+X["EnclosedPorch"]+X["3SsnPorch"]+X["ScreenPorch"]

    
            return X

pipe = Pipeline([
    ('labenc', labelenc()),
    ('add_feature', add_feature(additional=2)),
    ('skew_dummies', skew_dummies(skew=1)),
    ])

piped = pipe.fit_transform(all_data)
piped.shape
```




    (2917, 427)




```python
np.save("piped",piped)
np.save("y_raw",y_raw)
```


