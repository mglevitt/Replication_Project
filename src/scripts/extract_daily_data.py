import pandas as pd
import csv
import regex as re
import os
from pathlib import Path
import logging


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logging.warning('This message will get logged on to a file')

def convert_txt_to_df(tel):
    try:
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
        logging.info(f'The txt file for {tel} was successfully converted into a df.')
        return df
    except:
        logging.error(f'Unexpected error reached while converting the txt file for {tel} into a df.')

def create_tel_df():
    try:
        teleconnections = ['epo','nao','pna','wpo']
        dfs = []
        for t in teleconnections:
            df = convert_txt_to_df(t)
            dfs.append(df)
        combined_df = pd.concat(dfs)
        dates = ['year','month','day']
        for col in dates:
            combined_df[col] = combined_df[col].astype(int)
        sorted_df = combined_df.sort_values(by = dates)
        logging.info('Successfully created df with all teloconection monthly values.')
        return sorted_df
    except:
        logging.error('Unexpected error reached while creating df of all teleconnections.')
#print(combined_df.head())
#cwd = os.getcwd()
#file_path = f'{cwd}/src/data/daily_data.csv'
#combined_df.to_csv(file_path)

sorted_df = create_tel_df()


def extract_column_data(tel,start):
    try:
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
    except:
        logging.error(f'Unexpected error geting column data for {tel} at start of {start}.')

def create_csv(offset):
    try:
        data = {}
        if offset == 2:
            start = -22
            end = 17
        else:
            start = -15 - (offset * 3)
            end = 16
        teleconnections = ['epo','nao','pna','wpo']
        for tel in teleconnections:
            for i in range(start,end,offset):
                feature_data = extract_column_data(tel,i)
                feature_name = f'{tel}{str(i)}'
                data[feature_name] = feature_data
        df = pd.DataFrame(data)
        cwd = os.getcwd()
        file_name = f'temporal_offset_{str(offset)}_data.csv'
        file_path = f'{cwd}/src/final_data/{file_name}'
        df.to_csv(file_path)
        logging.info(f'Successfully made {file_name}')
    except:
        logging.error(f'Unexpected error making csv file for data with offset of {offset}.')

for i in range(1,4):
    #create_csv(i)
    logging.info(i)

