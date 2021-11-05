import pandas as pd
import csv
import regex as re
import os
from pathlib import Path

def convert_txt_to_csv(tel):
    file_name = f'{tel}.reanalysis.t10trunc.1948-present.txt'
    cwd = os.getcwd()
    file_path = f'{cwd}/src/data/teleconn/{file_name}'
    with open(file_path,'r') as f:
        lines = f.readlines()
    data = []
    pat = '[\d\.]+'
    for line in lines:
        t = re.findall(pat,line)
        data.append(t)
    df = pd.DataFrame(data)
    df = df.rename(columns={0:'year',1:'month',2:'day',3:'level'})
    df['tel'] = tel
    return df

teleconnections = ['epo','nao','pna','wpo']
dfs = []
for t in teleconnections:
    df = convert_txt_to_csv(t)
    dfs.append(df)
combined_df = pd.concat(dfs)
dates = ['year','month','day']
for col in dates:
    combined_df[col] = combined_df[col].astype(int)
#print(combined_df.head())
#cwd = os.getcwd()
#file_path = f'{cwd}/src/data/daily_data.csv'
#combined_df.to_csv(file_path)
sorted_df = combined_df.sort_values(by = dates)



def extract_column_data(tel,start):
    c_list = []
    def extract_data_for_year(year,start):
        cnt = 0
        dec_1_in = df[(df['year'] == year) & (df['month'] == 12) & (df['day'] == 1)].index[0]
        c_in = dec_1_in + start
        while cnt < 90:
            c_list.append(df.loc[c_in]['level'])
            c_in += 1
            cnt += 1
    df = sorted_df[sorted_df['tel']==tel]
    for year in range(1950,2011):
        extract_data_for_year(year,start)
    return c_list

def create_csv(offset):
    data = {}
    if offset == 2:
        start = -22
        end = 17
    else:
        start = -15 - (offset * 3)
        end = 16
    for tel in teleconnections:
        for i in range(start,end,offset):
            feature_data = extract_column_data(tel,i)
            feature_name = f'{tel}{str(i)}'
            data[feature_name] = feature_data
    df = pd.DataFrame(data)
    cwd = os.getcwd()
    file_name = f'temporal_offset_{str(offset)}_data.csv'
    file_path = f'{cwd}/src/data//{file_name}'
    df.to_csv(file_path)

for i in range(1,4):
    create_csv(i)

