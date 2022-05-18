import pandas as pd
import numpy as np
import json
import os


from hrvanalysis import remove_outliers, remove_ectopic_beats, interpolate_nan_values
from hrvanalysis import get_time_domain_features
from hrvanalysis import plot_psd
from hrvanalysis import plot_poincare

# 设置文件路径
rri_data_path = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/all_rri.json'
label_data_path = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/label/治疗前量表-1.xlsx'


def load_rri_data(path):
    '''
    load rri data from json file
    '''
    with open(path, 'r') as f:
        rri_data = json.load(f)
        
    return rri_data


def rri_prep(rri_list):
    '''
    对RRI数据进行预处理
    '''
    
    if len(rri_list) < 10:
        return [1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000]
    # This remove outliers from signal
    rr_intervals_without_outliers = remove_outliers(rr_intervals=rri_list,  
                                                    low_rri=300, high_rri=2000)
    # This replace outliers nan values with linear interpolation
    interpolated_rr_intervals = interpolate_nan_values(rr_intervals=rr_intervals_without_outliers,
                                                    interpolation_method="linear")

    # This remove ectopic beats from signal
    nn_intervals_list = remove_ectopic_beats(rr_intervals=interpolated_rr_intervals, method="malik")
    # This replace ectopic beats nan values with linear interpolation
    interpolated_nn_intervals = interpolate_nan_values(rr_intervals=nn_intervals_list)
    
    return interpolated_nn_intervals


# def get_time_domain_features(rri_list):
#     '''
#     从RRI数据中获取时域特征
#     '''
#     time_domain_features = get_time_domain_features(rri_list)
    
#     return time_domain_features

## 添加新的特征，待做
    
    
def load_label_data(path):
    '''
    load label data from excel file
    '''
    df = pd.read_excel(path)
    
    return df


def main():
    
    label_data = load_label_data(label_data_path)
    
    rri_data = load_rri_data(rri_data_path)
    
    # feature_df = pd.DataFrame(columns=['patient_id','mean_nni', 'sdnn', 'sdsd', 'nni_50', 'pnni_50', 'nni_20', 'pnni_20', 'rmssd', 'median_nni', 'range_nni', 'cvsd', 'cvnni', 'mean_hr', 'max_hr', 'min_hr', 'std_hr'])
    # feature_df = pd.DataFrame()
    
    feature_list = []
    for id, rri in rri_data.items():
        rri = rri_prep(rri)
        rri_features = get_time_domain_features(rri)
        rri_features['patient_id'] = id
        feature_list.append(rri_features)
    
    feature_df = pd.DataFrame(feature_list)
    print(feature_df)
        
    feature_df.to_csv('./data/feature_df.csv', index=False)

    
if __name__ == '__main__':
    main()