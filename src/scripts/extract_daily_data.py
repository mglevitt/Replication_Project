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
print(combined_df.head())
cwd = os.getcwd()
file_path = f'{cwd}/src/data/daily_data.csv'
combined_df.to_csv(file_path)