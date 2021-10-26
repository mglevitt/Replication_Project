import netCDF4
import numpy as np
import requests
import urllib
import os
import logging
from pathlib import Path


def download_file(year):
    try:
        file_name = f'hgt.{year}.nc'
        cwd = os.getcwd()
        file_path = f'{cwd}/src/data/{file_name}'
        if Path(file_path).exists():
            logging.info(f'Data for {year} is already downloaded.')
        else:
            url = 'https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis.dailyavgs/pressure/'
            file_url = f'{url}{file_name}'
            file = requests.get(file_url)
            
            
            open(f'src/data/{file_name}','wb').write(file.content)
            logging.info(f'Dara for {year} successfully downloaded.')

    except:
        logging.error('Unexpected error while downloading data from {year}.')


for i in range(2011 - 1950):
    yr = 1950 + i
    download_file(yr)

