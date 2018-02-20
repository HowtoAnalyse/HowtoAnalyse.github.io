import numpy as np
from sklearn.model_selection import train_test_split

def shaper(ar):
    newar = ar.reshape(ar.shape[0],-1).T
    return newar

def load_data(data_path):
    data = np.load(data_path)
    X_orig,y_orig=data[:,:-1],data[:,-1]
    X=shaper(X_orig)
    y=shaper(y_orig)
    print("X shape: {}".format(X.shape))
    print("y shape: {}".format(y.shape))
    return X,y

def load_train_test(data_path):
    trainX_orig,testX_orig,trainy_orig,testy_orig = train_test_split(data[:,:-1],data[:,-1])
    trainX = shaper(trainX_orig)
    trainy = shaper(trainy_orig)
    testX = shaper(testX_orig)
    testy = shaper(testy_orig)
    print("trainX shape: {}".format(trainX.shape))
    print("testX shape: {}".format(testX.shape))
    print("trainy shape: {}".format(trainy.shape))
    print("testy shape: {}".format(testy.shape))
    return trainX,trainy,testX,testy
