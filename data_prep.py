import os
import pandas as pd
import json
import utils

# define path and variables
data_dir = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/raw'
user_basic_info_path = '/home/ubuntu/working-dir/huawei_data-proj/心率变异性/data/用户基本信息.csv'



def read_csv(dir_path):
    '''
    read csv files in the dir_path, return one df
    '''
    
    file_list = os.listdir(dir_path)
    df_list = []
    
    for file in file_list:
        df = pd.read_csv(os.path.join(dir_path, file))
        df_list.append(df)
        
    long_df = pd.concat(df_list)
    long_df['recordtime'] = pd.to_datetime(long_df['recordtime'])
    
    return long_df


def change_user_id(df):
    '''
    change user_id to real_id
    '''
    user_id_dict = utils.get_user_id_dict(user_basic_info_path)
    df['healthid'] = df['healthid'].map(user_id_dict)
    return df


def get_df_dict_by_user_id(df):
    '''
    get df_dict by user_id
    '''
    df_dict = {}
    for user_id in df['healthid'].unique():
        df_dict[user_id] = df[df['healthid'] == user_id].sort_values('recordtime')
    return df_dict


def get_rri_list(df):
    '''
    get rri_list from df
    '''
    rri_list = []
    
    for index, row in df.iterrows():
        row_rri = json.loads(row['rri'])
        row_rri_list = []
        for item in row_rri:
            row_rri_list.append(item['rri']['value'])
            
        if df['recordtime'].iloc[index] - df['recordtime'].iloc[index-1] > 2:
            rri_list.append(row_rri_list)
    for rri in df['rriData']:
        rri = json.loads(rri)
        rri = [value['rri']['value'] for value in rri]
        rri_list.extend(rri)
        
    return rri_list


def main():
    
    raw_data = read_csv(data_dir)
    raw_data = change_user_id(raw_data)
    raw_dict = get_df_dict_by_user_id(raw_data)
    
    for key, value in raw_dict.items():
        rri_list = get_rri_list(value)
        raw_dict[key] = rri_list
        
    with open('./data/all_rri.json', 'w') as f:
        json.dump(raw_dict, f)

if __name__=="__main__":
    main()
