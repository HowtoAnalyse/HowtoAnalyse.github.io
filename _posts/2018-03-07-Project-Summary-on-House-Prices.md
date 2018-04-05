---
layout: post
title: Project Summary on House Prices
author: sara
categories: [Machine Learning]
image: assets/images/dogs/dog-hybrid-animal-lying-162349.jpeg
featured: False
---

# Helper Functions


```python
import numpy as np
import pandas as pd
from ggplot import *
from scipy.stats import skew

from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
from sklearn.preprocessing import LabelEncoder,RobustScaler, StandardScaler
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.decomposition import PCA
from sklearn.preprocessing import Imputer
from sklearn.model_selection import cross_val_score, GridSearchCV, KFold
from sklearn.linear_model import LinearRegression,Ridge,Lasso,ElasticNet, SGDRegressor, BayesianRidge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import SVR, LinearSVR
from sklearn.kernel_ridge import KernelRidge
# from xgboost import XGBRegressor

train = pd.read_csv('train.csv')
test = pd.read_csv('test.csv')

class stacking(BaseEstimator, RegressorMixin, TransformerMixin):
    def __init__(self,mod,meta_model):
        self.mod = mod
        self.meta_model = meta_model
        self.kf = KFold(n_splits=5, random_state=42, shuffle=True)
        
    def fit(self,X,y):
        self.saved_model = [list() for i in self.mod]
        oof_train = np.zeros((X.shape[0], len(self.mod)))
        
        for i,model in enumerate(self.mod):
            for train_index, val_index in self.kf.split(X,y):
                renew_model = clone(model)
                renew_model.fit(X[train_index], y[train_index])
                self.saved_model[i].append(renew_model)
                oof_train[val_index,i] = renew_model.predict(X[val_index])
        
        self.meta_model.fit(oof_train,y)
        return self
    
    def predict(self,X):
        whole_test = np.column_stack([np.column_stack(model.predict(X) for model in single_model).mean(axis=1) 
                                      for single_model in self.saved_model]) 
        return self.meta_model.predict(whole_test)
    
    def get_oof(self,X,y,test_X):
        oof = np.zeros((X.shape[0],len(self.mod)))
        test_single = np.zeros((test_X.shape[0],5))
        test_mean = np.zeros((test_X.shape[0],len(self.mod)))
        for i,model in enumerate(self.mod):
            for j, (train_index,val_index) in enumerate(self.kf.split(X,y)):
                clone_model = clone(model)
                clone_model.fit(X[train_index],y[train_index])
                oof[val_index,i] = clone_model.predict(X[val_index])
                test_single[:,j] = clone_model.predict(test_X)
            test_mean[:,i] = test_single.mean(axis=1)
        return oof, test_mean

class grid():
    def __init__(self,model):
        self.model = model
    
    def grid_get(self,X,y,param_grid):
        grid_search = GridSearchCV(self.model,param_grid,cv=5, scoring="neg_mean_squared_error")
        grid_search.fit(X,y)
        print(grid_search.best_params_, np.sqrt(-grid_search.best_score_))
        grid_search.cv_results_['mean_test_score'] = np.sqrt(-grid_search.cv_results_['mean_test_score'])
        print(pd.DataFrame(grid_search.cv_results_)[['params','mean_test_score','std_test_score']])
        
def rmse_cv(model,X,y):
    rmse = np.sqrt(-cross_val_score(model, X, y, scoring="neg_mean_squared_error", cv=10))
    return rmse


```

    /anaconda3/lib/python3.6/site-packages/ggplot/utils.py:81: FutureWarning: pandas.tslib is deprecated and will be removed in a future version.
    You can access Timestamp as pandas.Timestamp
      pd.tslib.Timestamp,
    /anaconda3/lib/python3.6/site-packages/ggplot/stats/smoothers.py:4: FutureWarning: The pandas.lib module is deprecated and will be removed in a future version. These are private functions and can be accessed from pandas._libs.lib instead
      from pandas.lib import Timestamp
    /anaconda3/lib/python3.6/site-packages/statsmodels/compat/pandas.py:56: FutureWarning: The pandas.core.datetools module is deprecated and will be removed in a future version. Please use the pandas.tseries module instead.
      from pandas.core import datetools


## Exploratory Analysis

1. Distribution of the dependent variable HousePrice
2. Missing values
3. Correlation
4. Random exploration of each feature

#### Some discoveries
* Recently built houses tend to have higher prices.
* There are 2 outliers with extremely large GrLivArea values.


```python
ggplot(aes(x='YearBuilt', y='SalePrice'), data=train) +\
    geom_line() +\
    stat_smooth(colour='blue', span=50)
```


    ---------------------------------------------------------------------------

    AttributeError                            Traceback (most recent call last)

    /anaconda3/lib/python3.6/site-packages/IPython/core/formatters.py in __call__(self, obj)
        700                 type_pprinters=self.type_printers,
        701                 deferred_pprinters=self.deferred_printers)
    --> 702             printer.pretty(obj)
        703             printer.flush()
        704             return stream.getvalue()


    /anaconda3/lib/python3.6/site-packages/IPython/lib/pretty.py in pretty(self, obj)
        393                             if callable(meth):
        394                                 return meth(obj, self, cycle)
    --> 395             return _default_pprint(obj, self, cycle)
        396         finally:
        397             self.end_group()


    /anaconda3/lib/python3.6/site-packages/IPython/lib/pretty.py in _default_pprint(obj, p, cycle)
        508     if _safe_getattr(klass, '__repr__', None) is not object.__repr__:
        509         # A user-provided repr. Find newlines and replace them with p.break_()
    --> 510         _repr_pprint(obj, p, cycle)
        511         return
        512     p.begin_group(1, '<')


    /anaconda3/lib/python3.6/site-packages/IPython/lib/pretty.py in _repr_pprint(obj, p, cycle)
        699     """A pprint that just redirects to the normal repr function."""
        700     # Find newlines and replace them with p.break_()
    --> 701     output = repr(obj)
        702     for idx,output_line in enumerate(output.splitlines()):
        703         if idx:


    /anaconda3/lib/python3.6/site-packages/ggplot/ggplot.py in __repr__(self)
        114 
        115     def __repr__(self):
    --> 116         self.make()
        117         # this is nice for dev but not the best for "real"
        118         if os.environ.get("GGPLOT_DEV"):


    /anaconda3/lib/python3.6/site-packages/ggplot/ggplot.py in make(self)
        634                         if kwargs==False:
        635                             continue
    --> 636                         layer.plot(ax, facetgroup, self._aes, **kwargs)
        637 
        638             self.apply_limits()


    /anaconda3/lib/python3.6/site-packages/ggplot/stats/stat_smooth.py in plot(self, ax, data, _aes)
         75 
         76         smoothed_data = pd.DataFrame(dict(x=x, y=y, y1=y1, y2=y2))
    ---> 77         smoothed_data = smoothed_data.sort('x')
         78 
         79         params = self._get_plot_args(data, _aes)


    /anaconda3/lib/python3.6/site-packages/pandas/core/generic.py in __getattr__(self, name)
       3612             if name in self._info_axis:
       3613                 return self[name]
    -> 3614             return object.__getattribute__(self, name)
       3615 
       3616     def __setattr__(self, name, value):


    AttributeError: 'DataFrame' object has no attribute 'sort'



![png](output_3_1.png)



```python
train.drop(train[(train["GrLivArea"]>4000)&(train["SalePrice"]<300000)].index,inplace=True)
full=pd.concat([train,test], ignore_index=True)
full.drop(['Id'],axis=1, inplace=True)
```

Plots have been removed in printed edition.

## Data Cleaning

The missing value imputation techniques I used:
* Fill in the NAs of LotFrontage based on the median of LotArea and Neighborhood
* kNN
* Fill in the rest of missing values with mode (the most frequently appearing value), 0 for numerical features and "None" for categorical ones according to data description.


```python
full["LotAreaCut"] = pd.qcut(full.LotArea,10)
full['LotFrontage_1']=full.groupby(['LotAreaCut','Neighborhood'])['LotFrontage'].transform(lambda x: x.fillna(x.median()))
full['LotFrontage_2']=full.groupby(['LotAreaCut'])['LotFrontage_1'].transform(lambda x: x.fillna(x.median()))
full.drop(['LotFrontage','LotFrontage_1'],axis=1,inplace=True)

```


```python
full_cat = full.select_dtypes(include=["object"])
full_num = full.select_dtypes(exclude=["object"])
# mode_cols = full_cat.columns[full_cat.isnull().sum() != 0].tolist()
# median_cols = full_num.columns[full_num.isnull().sum() != 0].tolist()
# median_cols.remove('SalePrice')
```


```python
mode_cols = ["MSZoning", "BsmtFullBath", "BsmtHalfBath", "Utilities", "Functional", "Electrical", "KitchenQual", "SaleType","Exterior1st", "Exterior2nd"]
for col in mode_cols:
    full[col].fillna(full[col].mode()[0], inplace=True)

cat_cols = ["PoolQC" , "MiscFeature", "Alley", "Fence", "FireplaceQu", "GarageQual", "GarageCond", "GarageFinish", "GarageYrBlt", "GarageType", "BsmtExposure", "BsmtCond", "BsmtQual", "BsmtFinType2", "BsmtFinType1", "MasVnrType"]
for col in cat_cols:
    full[col].fillna("None", inplace=True)

num_cols = ["MasVnrArea", "BsmtUnfSF", "TotalBsmtSF", "GarageCars", "BsmtFinSF2", "BsmtFinSF1", "GarageArea"]
for col in num_cols:
    full[col].fillna(0, inplace=True)
```

## Feature Engineering

* Some numerical features have been converted into categorical ones, followed by encoding.
* Encode each categorical feature by mapping its unique values to different numbers using *LabelEncoding*, *Frequency Encoding*, *One-hot Encoding* or *Target-driven Encoding* (group SalePrice by one feature and sort it based on mean and median) --todo
* Apply log1p to skewed features --todo
* Scaling data using RobustScaler()
* Inspired by [TensorFlow Wide & Deep Learning](https://www.tensorflow.org/tutorials/wide_and_deep), I generated crossed feature columns in order by memorize sparse interactions between features effectively
* PCA, multicollinearity


```python
NumStr = ["MSSubClass","BsmtFullBath","BsmtHalfBath","HalfBath","BedroomAbvGr","KitchenAbvGr","MoSold","YrSold","YearBuilt","YearRemodAdd","LowQualFinSF","GarageYrBlt"]
for col in NumStr:
    full[col]=full[col].astype(str)

def map_values():
    full["oMSSubClass"] = full.MSSubClass.map({'180':1, 
                                        '30':2, '45':2, 
                                        '190':3, '50':3, '90':3, 
                                        '85':4, '40':4, '160':4, 
                                        '70':5, '20':5, '75':5, '80':5, '150':5,
                                        '120': 6, '60':6})
    
    full["oMSZoning"] = full.MSZoning.map({'C (all)':1, 'RH':2, 'RM':2, 'RL':3, 'FV':4})
    
    full["oNeighborhood"] = full.Neighborhood.map({'MeadowV':1,
                                               'IDOTRR':2, 'BrDale':2,
                                               'OldTown':3, 'Edwards':3, 'BrkSide':3,
                                               'Sawyer':4, 'Blueste':4, 'SWISU':4, 'NAmes':4,
                                               'NPkVill':5, 'Mitchel':5,
                                               'SawyerW':6, 'Gilbert':6, 'NWAmes':6,
                                               'Blmngtn':7, 'CollgCr':7, 'ClearCr':7, 'Crawfor':7,
                                               'Veenker':8, 'Somerst':8, 'Timber':8,
                                               'StoneBr':9,
                                               'NoRidge':10, 'NridgHt':10})
    
    full["oCondition1"] = full.Condition1.map({'Artery':1,
                                           'Feedr':2, 'RRAe':2,
                                           'Norm':3, 'RRAn':3,
                                           'PosN':4, 'RRNe':4,
                                           'PosA':5 ,'RRNn':5})
    
    full["oBldgType"] = full.BldgType.map({'2fmCon':1, 'Duplex':1, 'Twnhs':1, '1Fam':2, 'TwnhsE':2})
    
    full["oHouseStyle"] = full.HouseStyle.map({'1.5Unf':1, 
                                           '1.5Fin':2, '2.5Unf':2, 'SFoyer':2, 
                                           '1Story':3, 'SLvl':3,
                                           '2Story':4, '2.5Fin':4})
    
    full["oExterior1st"] = full.Exterior1st.map({'BrkComm':1,
                                             'AsphShn':2, 'CBlock':2, 'AsbShng':2,
                                             'WdShing':3, 'Wd Sdng':3, 'MetalSd':3, 'Stucco':3, 'HdBoard':3,
                                             'BrkFace':4, 'Plywood':4,
                                             'VinylSd':5,
                                             'CemntBd':6,
                                             'Stone':7, 'ImStucc':7})
    
    full["oMasVnrType"] = full.MasVnrType.map({'BrkCmn':1, 'None':1, 'BrkFace':2, 'Stone':3})
    
    full["oExterQual"] = full.ExterQual.map({'Fa':1, 'TA':2, 'Gd':3, 'Ex':4})
    
    full["oFoundation"] = full.Foundation.map({'Slab':1, 
                                           'BrkTil':2, 'CBlock':2, 'Stone':2,
                                           'Wood':3, 'PConc':4})
    
    full["oBsmtQual"] = full.BsmtQual.map({'Fa':2, 'None':1, 'TA':3, 'Gd':4, 'Ex':5})
    
    full["oBsmtExposure"] = full.BsmtExposure.map({'None':1, 'No':2, 'Av':3, 'Mn':3, 'Gd':4})
    
    full["oHeating"] = full.Heating.map({'Floor':1, 'Grav':1, 'Wall':2, 'OthW':3, 'GasW':4, 'GasA':5})
    
    full["oHeatingQC"] = full.HeatingQC.map({'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
    
    full["oKitchenQual"] = full.KitchenQual.map({'Fa':1, 'TA':2, 'Gd':3, 'Ex':4})
    
    full["oFunctional"] = full.Functional.map({'Maj2':1, 'Maj1':2, 'Min1':2, 'Min2':2, 'Mod':2, 'Sev':2, 'Typ':3})
    
    full["oFireplaceQu"] = full.FireplaceQu.map({'None':1, 'Po':1, 'Fa':2, 'TA':3, 'Gd':4, 'Ex':5})
    
    full["oGarageType"] = full.GarageType.map({'CarPort':1, 'None':1,
                                           'Detchd':2,
                                           '2Types':3, 'Basment':3,
                                           'Attchd':4, 'BuiltIn':5})
    
    full["oGarageFinish"] = full.GarageFinish.map({'None':1, 'Unf':2, 'RFn':3, 'Fin':4})
    
    full["oPavedDrive"] = full.PavedDrive.map({'N':1, 'P':2, 'Y':3})
    
    full["oSaleType"] = full.SaleType.map({'COD':1, 'ConLD':1, 'ConLI':1, 'ConLw':1, 'Oth':1, 'WD':1,
                                       'CWD':2, 'Con':3, 'New':3})
    
    full["oSaleCondition"] = full.SaleCondition.map({'AdjLand':1, 'Abnorml':2, 'Alloca':2, 'Family':2, 'Normal':3, 'Partial':4})            
    return "Done!"

map_values()
full.drop("LotAreaCut",axis=1,inplace=True)
full.drop(['SalePrice'],axis=1,inplace=True)

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
full_pipe = pipe.fit_transform(full)
n_train=train.shape[0]
X = full_pipe[:n_train]
test_X = full_pipe[n_train:]
y= train.SalePrice
scaler = RobustScaler()
X_scaled = scaler.fit(X).transform(X)
y_log = np.log(train.SalePrice)
test_X_scaled = scaler.transform(test_X)
pca = PCA(n_components=410)
X_scaled=pca.fit_transform(X_scaled)
test_X_scaled = pca.transform(test_X_scaled)
```

## Model training & Evaluation

1. Choose from 13 models using 10-fold cross-validation  
2. Parameter tuning using gridsearch.


```python
models = [LinearRegression(),Ridge(),Lasso(alpha=0.01,max_iter=10000),RandomForestRegressor(),GradientBoostingRegressor(),SVR(),LinearSVR(),
          ElasticNet(alpha=0.001,max_iter=10000),SGDRegressor(max_iter=1000,tol=1e-3),BayesianRidge(),KernelRidge(alpha=0.6, kernel='polynomial', degree=2, coef0=2.5),
          ExtraTreesRegressor()
#           ,XGBRegressor()
         ]

names = ["LR", "Ridge", "Lasso", "RF", "GBR", "SVR", "LinSVR", "Ela","SGD","Bay","Ker","Extra"
#          ,"Xgb"
        ]
for name, model in zip(names, models):
    score = rmse_cv(model, X_scaled, y_log)
    print("{}: {:.6f}, {:.4f}".format(name,score.mean(),score.std()))

```

    LR: 1290126350.109342, 764360825.3095
    Ridge: 0.113003, 0.0158
    Lasso: 0.120975, 0.0138
    RF: 0.138568, 0.0144
    GBR: 0.124585, 0.0144
    SVR: 0.110569, 0.0141
    LinSVR: 0.116373, 0.0158
    Ela: 0.108113, 0.0137
    SGD: 0.153181, 0.0113
    Bay: 0.107870, 0.0138
    Ker: 0.106972, 0.0138
    Extra: 0.136361, 0.0109



```python
grid(Lasso()).grid_get(X_scaled,y_log,{'alpha': [0.0004,0.0005,0.0007,0.0009],'max_iter':[10000]})
grid(Ridge()).grid_get(X_scaled,y_log,{'alpha':[35,40,45,50,55,60,65,70,80,90]})
grid(SVR()).grid_get(X_scaled,y_log,{'C':[11,13,15],'kernel':["rbf"],"gamma":[0.0003,0.0004],"epsilon":[0.008,0.009]})
param_grid={'alpha':[0.2,0.3,0.4], 'kernel':["polynomial"], 'degree':[3],'coef0':[0.8,1]}
grid(KernelRidge()).grid_get(X_scaled,y_log,param_grid)
grid(ElasticNet()).grid_get(X_scaled,y_log,{'alpha':[0.0008,0.004,0.005],'l1_ratio':[0.08,0.1,0.3],'max_iter':[10000]})
```

    {'alpha': 0.0005, 'max_iter': 10000} 0.11129660796478758
                                     params  mean_test_score  std_test_score
    0  {'alpha': 0.0004, 'max_iter': 10000}         0.111463        0.001392
    1  {'alpha': 0.0005, 'max_iter': 10000}         0.111297        0.001339
    2  {'alpha': 0.0007, 'max_iter': 10000}         0.111538        0.001284
    3  {'alpha': 0.0009, 'max_iter': 10000}         0.111915        0.001206


    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('mean_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split0_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split1_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split2_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split3_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split4_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('std_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)


    {'alpha': 60} 0.11020174961498394
              params  mean_test_score  std_test_score
    0  {'alpha': 35}         0.110375        0.001268
    1  {'alpha': 40}         0.110305        0.001249
    2  {'alpha': 45}         0.110258        0.001235
    3  {'alpha': 50}         0.110227        0.001223
    4  {'alpha': 55}         0.110209        0.001213
    5  {'alpha': 60}         0.110202        0.001205
    6  {'alpha': 65}         0.110203        0.001198
    7  {'alpha': 70}         0.110212        0.001192
    8  {'alpha': 80}         0.110247        0.001184
    9  {'alpha': 90}         0.110301        0.001178


    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('mean_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split0_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split1_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split2_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split3_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split4_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('std_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)


    {'C': 13, 'epsilon': 0.009, 'gamma': 0.0004, 'kernel': 'rbf'} 0.10823195916311673
                                                   params  mean_test_score  \
    0   {'C': 11, 'epsilon': 0.008, 'gamma': 0.0003, '...         0.108661   
    1   {'C': 11, 'epsilon': 0.008, 'gamma': 0.0004, '...         0.108312   
    2   {'C': 11, 'epsilon': 0.009, 'gamma': 0.0003, '...         0.108650   
    3   {'C': 11, 'epsilon': 0.009, 'gamma': 0.0004, '...         0.108297   
    4   {'C': 13, 'epsilon': 0.008, 'gamma': 0.0003, '...         0.108562   
    5   {'C': 13, 'epsilon': 0.008, 'gamma': 0.0004, '...         0.108248   
    6   {'C': 13, 'epsilon': 0.009, 'gamma': 0.0003, '...         0.108555   
    7   {'C': 13, 'epsilon': 0.009, 'gamma': 0.0004, '...         0.108232   
    8   {'C': 15, 'epsilon': 0.008, 'gamma': 0.0003, '...         0.108474   
    9   {'C': 15, 'epsilon': 0.008, 'gamma': 0.0004, '...         0.108248   
    10  {'C': 15, 'epsilon': 0.009, 'gamma': 0.0003, '...         0.108444   
    11  {'C': 15, 'epsilon': 0.009, 'gamma': 0.0004, '...         0.108251   
    
        std_test_score  
    0         0.001553  
    1         0.001609  
    2         0.001555  
    3         0.001607  
    4         0.001601  
    5         0.001615  
    6         0.001602  
    7         0.001621  
    8         0.001629  
    9         0.001609  
    10        0.001633  
    11        0.001617  


    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('mean_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split0_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split1_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split2_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split3_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split4_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('std_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)


    {'alpha': 0.2, 'coef0': 0.8, 'degree': 3, 'kernel': 'polynomial'} 0.10826973614765915
                                                  params  mean_test_score  \
    0  {'alpha': 0.2, 'coef0': 0.8, 'degree': 3, 'ker...         0.108270   
    1  {'alpha': 0.2, 'coef0': 1, 'degree': 3, 'kerne...         0.108509   
    2  {'alpha': 0.3, 'coef0': 0.8, 'degree': 3, 'ker...         0.108399   
    3  {'alpha': 0.3, 'coef0': 1, 'degree': 3, 'kerne...         0.108278   
    4  {'alpha': 0.4, 'coef0': 0.8, 'degree': 3, 'ker...         0.108762   
    5  {'alpha': 0.4, 'coef0': 1, 'degree': 3, 'kerne...         0.108299   
    
       std_test_score  
    0        0.001209  
    1        0.001243  
    2        0.001189  
    3        0.001210  
    4        0.001181  
    5        0.001191  


    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('mean_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split0_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split1_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split2_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split3_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split4_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('std_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)


    {'alpha': 0.005, 'l1_ratio': 0.08, 'max_iter': 10000} 0.11117135158453595
                                                  params  mean_test_score  \
    0  {'alpha': 0.0008, 'l1_ratio': 0.08, 'max_iter'...         0.114762   
    1  {'alpha': 0.0008, 'l1_ratio': 0.1, 'max_iter':...         0.114250   
    2  {'alpha': 0.0008, 'l1_ratio': 0.3, 'max_iter':...         0.112062   
    3  {'alpha': 0.004, 'l1_ratio': 0.08, 'max_iter':...         0.111278   
    4  {'alpha': 0.004, 'l1_ratio': 0.1, 'max_iter': ...         0.111209   
    5  {'alpha': 0.004, 'l1_ratio': 0.3, 'max_iter': ...         0.112483   
    6  {'alpha': 0.005, 'l1_ratio': 0.08, 'max_iter':...         0.111171   
    7  {'alpha': 0.005, 'l1_ratio': 0.1, 'max_iter': ...         0.111192   
    8  {'alpha': 0.005, 'l1_ratio': 0.3, 'max_iter': ...         0.112983   
    
       std_test_score  
    0        0.001937  
    1        0.001904  
    2        0.001596  
    3        0.001382  
    4        0.001326  
    5        0.001160  
    6        0.001312  
    7        0.001277  
    8        0.001159  


    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('mean_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split0_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split1_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split2_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split3_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('split4_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)
    /anaconda3/lib/python3.6/site-packages/sklearn/utils/deprecation.py:122: FutureWarning: You are accessing a training score ('std_train_score'), which will not be available by default any more in 0.21. If you need training scores, please set return_train_score=True
      warnings.warn(*warn_args, **warn_kwargs)


## Stacking

The ensemble methods I have tried:
1. weighted average
2. stacking (the final model I use)


```python
a = Imputer().fit_transform(X_scaled)
b = Imputer().fit_transform(y_log.values.reshape(-1,1)).ravel()
lasso = Lasso(alpha=0.0005,max_iter=10000)
ridge = Ridge(alpha=60)
svr = SVR(gamma= 0.0004,kernel='rbf',C=13,epsilon=0.009)
ker = KernelRidge(alpha=0.2 ,kernel='polynomial',degree=3 , coef0=0.8)
ela = ElasticNet(alpha=0.005,l1_ratio=0.08,max_iter=10000)
bay = BayesianRidge()
stack_model = stacking(mod=[lasso,ridge,svr,ker,ela,bay],meta_model=ker)
X_train_stack, X_test_stack = stack_model.get_oof(a,b,test_X_scaled)
X_train_add = np.hstack((a,X_train_stack))
X_test_add = np.hstack((test_X_scaled,X_test_stack))
# stack_model.fit(X_train_add,b)
# pred = np.exp(stack_model.predict(X_test_add))
stack_model.fit(a,b)
pred = np.exp(stack_model.predict(test_X_scaled))
submission = pd.DataFrame({'Id':test.Id, 'SalePrice':pred})
submName = strftime("%Y%m%d%H%M%S", gmtime()) + "_submission.csv"
submission.to_csv(submName, index=False)
```


    ---------------------------------------------------------------------------

    NameError                                 Traceback (most recent call last)

    <ipython-input-10-6a041feb205d> in <module>()
         16 pred = np.exp(stack_model.predict(test_X_scaled))
         17 submission = pd.DataFrame({'Id':test.Id, 'SalePrice':pred})
    ---> 18 submName = strftime("%Y%m%d%H%M%S", gmtime()) + "_submission.csv"
         19 submission.to_csv(submName, index=False)


    NameError: name 'strftime' is not defined






# Reference

*  [TensorFlow Wide & Deep Learning](https://www.tensorflow.org/tutorials/wide_and_deep)
* [A Kaggler's Guide to Model Stacking in Practice](http://blog.kaggle.com/2016/12/27/a-kagglers-guide-to-model-stacking-in-practice/)




