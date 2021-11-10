import pandas as pd
import csv
import regex as re
import os
from pathlib import Path


def convert_txt_to_csv(tel):
    file_name = f'{tel}_monthly_avgs.txt'
    cwd = os.getcwd()
    file_path = f'{cwd}/src/data/monthly/{file_name}'
    with open(file_path,'r') as f:
        lines = f.readlines()
    data = []
    pat = '[\d\.]+'
    cnt = 1
    for line in lines:
        if cnt == 13:
            cnt = 1
        year = line[:5]
        t = [year,cnt]
        cnt +=1
        lev = re.findall(pat,line[5:])
        t.append(lev[-1])
        data.append(t)
    df = pd.DataFrame(data)
    df = df.rename(columns={0:'year',1:'month',2:'level'})
    df['tel'] = tel
    return df

teleconnections = ['epo','nao','pna','wpo','enso']
dfs = []
for tl in teleconnections:
    df = convert_txt_to_csv(tl)
    dfs.append(df)
combined_df = pd.concat(dfs)
#print(combined_df.head())
cwd = os.getcwd()
file_path = f'{cwd}/src/data/monthly_data.csv'
djf_file_path = f'{cwd}/src/final_data/monthly_djf_data.csv'
combined_df.to_csv(file_path)

enso_df = combined_df[combined_df['tel'] == 'enso']

cwd = os.getcwd()
file_path = f'{cwd}/src/data/averaged_monthly_data.csv'

df = pd.read_csv(f'{cwd}/src/data/daily_data.csv')
grouped_df = df.groupby(['year','month','tel']).mean()
monthly_df = grouped_df.reset_index().drop(columns = ['Unnamed: 0','day'])
monthly_df = pd.concat([monthly_df,enso_df])
def convert_to_int(x):
    try:
        x = x.replace(' ','')
        return int(x)
    except:
        return int(x)
monthly_df['year'] = monthly_df[['year']].applymap(convert_to_int)
monthly_df = monthly_df[(monthly_df['year'] >= 1950)  & (monthly_df['year'] <= 2012)]
#print(monthly_df.shape)
djf_df = monthly_df.loc[monthly_df['month'].isin([12,1,2])]
#print(monthly_df.head())
#print(djf_df.head())

def extract_date(x):
    x['date'] =  str(x['year']) + ' ,' + str(x['month'])
    return x

djf_df = djf_df.apply(extract_date, axis = 1)
djf_df = djf_df.sort_values(by = ['date'])
data = {}
for tel in teleconnections:
    data[tel] = djf_df[djf_df['tel'] == tel]['level'].tolist()
new_djf_df = pd.DataFrame(data)
new_djf_df['date'] = djf_df[djf_df['tel'] == 'enso']['date'].tolist()
new_djf_df = new_djf_df.set_index('date')
#new_djf_df = djf_df.pivot_table(values = 'level', index = 'date',columns = 'tel')
#print(new_djf_df.head())
monthly_df.to_csv(file_path)
new_djf_df.to_csv(djf_file_path)

