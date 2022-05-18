from cProfile import label
import os
import json
import pandas as pd

def get_user_id_dict(path):
    '''
    get user_id <-> real_id dict
    '''
    dic = {}
    user_df = pd.read_csv(path)
    dic = dict(zip(user_df['用户ID'], user_df['外部ID']))
    
    return dic

def merge_hrv_label_df(hrv_df, label_df):
    '''
    merge hrv_df and label_df
    '''
    df = pd.merge(hrv_df, label_df, on='patient_id', how='left')
    return df



if __name__=='__main__':
    
    label_data_path = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/label/治疗前量表-1.xlsx'
    hrv_data_path = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/feature_df.csv'
    
    label_df = pd.read_excel(label_data_path)
    hrv_df = pd.read_csv(hrv_data_path)
    
    #rename column
    label_df = label_df.rename(columns={'手环编号':'patient_id'})
    
    merge_df = merge_hrv_label_df(hrv_df, label_df)
    
    merge_df.to_csv('./data/merge_df.csv', index=False)