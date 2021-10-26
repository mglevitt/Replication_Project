import netCDF4
import numpy as np
import requests
import urllib
import os
import logging
from pathlib import Path

def read_nc_file(year):
    try:
        #reads the file 
        file_name = f'hgt.{year}.nc'
        cwd = os.getcwd()
        file_path = f'{cwd}/src/data/{file_name}'
        f = netCDF4.Dataset(file_path)
        print(f)

        #get the variable names
        print(f.variables.keys())

        hgt = f.variables['hgt'] # hgt variable
        print(hgt)
        logging.info('Successfully read data from {year}.')
    except:
        logging.error('Unexpected error while reading data from {year}.')

read_nc_file(1948)