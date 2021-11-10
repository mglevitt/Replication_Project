import pandas as pd
import csv
import regex as re
import os
from pathlib import Path
import logging


logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logging.warning('This message will get logged on to a file')

teleconnections = ['epo','nao','pna','wpo','enso']

def convert_txt_to_df(tel):
    try:
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
        logging.info(f'Successfully made df for {tel}.')
        return df
    except:
        logging.error('Unexpected error making df for {tel}.')

def create_combined_monthly_df():
    try:
        
        dfs = []
        for tl in teleconnections:
            df = convert_txt_to_df(tl)
            dfs.append(df)
        combined_df = pd.concat(dfs)
        #print(combined_df.head())
        enso_df = combined_df[combined_df['tel'] == 'enso']

        cwd = os.getcwd()
        daily_file_path = f'{cwd}/src/data/daily_data.csv'

        df = pd.read_csv(daily_file_path)
        grouped_df = df.groupby(['year','month','tel']).mean()
        monthly_df = grouped_df.reset_index().drop(columns = ['Unnamed: 0','day'])
        monthly_df = pd.concat([monthly_df,enso_df])
        logging.info('Successfully created monthly data df.')
        return monthly_df
    except:
        logging.error('Unexpected error reached creating monthly df.')


def clean_monthly_df(df):
    def convert_to_int(x):
        try:
            x = x.replace(' ','')
            return int(x)
        except:
            return int(x)
    try:
        df['year'] = df[['year']].applymap(convert_to_int)
        df = df[(df['year'] >= 1950)  & (df['year'] <= 2012)]
        logging.info('Successfully cleaned df.')
        return df
    except:
        logging.error('Unexpected error reached cleaning df.')

def clean_djf_df(df):
    def extract_date(x):
        try:
            x['date'] =  str(x['year']) + ' ,' + str(x['month'])
            return x
        except:
            logging.error('Unexpected error creating new date value.')
    try:
        df = df.loc[df['month'].isin([12,1,2])]
        df = df.apply(extract_date, axis = 1)
        df = df.sort_values(by = ['date'])
        logging.info('Successfully changed monthly df into djf df.')
        return df
    except:
        logging.error('Unexpected error reached changing monthly df into djf df.')

def create_final_djf_df(df):
    try:
        data = {}
        for tel in teleconnections:
            data[tel] = df[df['tel'] == tel]['level'].tolist()
        new_djf_df = pd.DataFrame(data)
        new_djf_df['date'] = df[df['tel'] == 'enso']['date'].tolist()
        new_djf_df = new_djf_df.set_index('date')
        logging.info('Successfully created final djf df.')
        return new_djf_df
    except:
        logging.error('Unexpected error reached creating final djf df.')


def create_monthly_csvs():
    try:
        monthly_df = create_combined_monthly_df()
        c_monthly_df = clean_monthly_df(monthly_df)
        djf_df = clean_djf_df(c_monthly_df)
        f_djf_df = create_final_djf_df(djf_df)

        cwd = os.getcwd()
        file_path = f'{cwd}/src/data/monthly_data.csv'
        djf_file_path = f'{cwd}/src/data/monthly_djf_data.csv'
        f_djf_file_path = f'{cwd}/src/final_data/monthly_djf_data.csv'

        c_monthly_df.to_csv(file_path)
        djf_df.to_csv(djf_file_path)
        f_djf_df.to_csv(f_djf_file_path)
        logging.info('Successfully created all monthly csvs.')
    except:
        logging.error('Unexpected error reached creating all monthly csvs.')

create_monthly_csvs()





