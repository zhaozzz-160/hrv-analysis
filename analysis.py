from operator import index, mod
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn import linear_model
from sklearn.linear_model import SGDRegressor
from sklearn.kernel_ridge import KernelRidge
from sklearn.linear_model import ElasticNet
from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import SVC
import pandas as pd
import os
import numpy as np
import logging
from matplotlib import pyplot as plt

def fit_model(X, y):
    """
    Fits a linear model to the given data.
    """
    model = linear_model.LinearRegression()
    model.fit(X, y)
    print(type(model).__name__)
    return model

def read_data(path):
    df = pd.read_csv(path)
    df = df.fillna(df.mean())
    return df 

def main():
    
    df = read_data('./data/merge_df.csv')
    
    X = df[['mean_nni', 'sdnn', 'sdsd', 'nni_50', 'pnni_50', 'nni_20', 'pnni_20', 'rmssd', 'median_nni', 'range_nni', 'cvsd', 'cvnni', 'mean_hr', 'max_hr', 'min_hr', 'std_hr']]
    y = df[['抑郁得分', '焦虑得分', '压力得分', '失眠得分', '自杀得分']]
    
    for y_name in y.columns:
        
        y_data = y[y_name]
        print(y_name)
        # print(X)
        model = fit_model(X, y_data)
        print('r2_score: ', r2_score(y_data, model.predict(X)))
        print('MAE: ', mean_absolute_error(y_data, model.predict(X)))
    
    y_1 = y[['抑郁得分']]
    
    for index, X_name in enumerate(X.columns):
        X_1 = X[[X_name]]
        model_1 = fit_model(X_1, y_1)
        plt.subplot(4, 4, index + 1)
        plt.scatter(X_1, y_1)
        plt.plot(X_1, model_1.predict(X_1))
        plt.title(X_name)
    # set 4:3 ratio and high dpi
    plt.gcf().set_size_inches(12, 9)
    plt.show()
    
    # for y_name in y.columns:
        
    #     for index, X_name in enumerate(X.columns):
            
    #         X_data = X[[X_name]]
    #         y_data = y[[y_name]]
    #         print(X_name, y_name)
    #         model = fit_model(X_data, y_data)
    #         plt.subplot(4, 4, index+1)
    #         plt.scatter(X_data, y_data)
    #         plt.plot(X_data, y_data, model.predict(X_data), color='red')
    #         plt.title(X_name + ' ' + y_name)
            
    #     plt.show()
    
    
if __name__ == '__main__':
    main()