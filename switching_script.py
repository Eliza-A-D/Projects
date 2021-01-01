# -*- coding: utf-8 -*-
"""
Created on Fri Mar 20 13:59:00 2020

@author: Eliza
"""

##switching between models depending on accuracy
import os
path = '/home/wind/wind_accuracy'
path1 = os.getcwd()
try:
    os.chdir(path)
except:
    print('Path not found!')
    os.chdir(path1)

try:
    import pandas as pd
    import requests
    from datetime import datetime
    from datetime import timedelta
    import numpy as np
    try:
        import magic
    except:
        print('magic has not installed in your machine!')
        pass
    import base64
    import time
    import json
    os.environ['TZ'] = 'Asia/Calcutta'
    try:
        time.tzset()
    except Exception as e:
        print(e)
        print('You are running this script on local machine thats why it is giving you an error.')
        pass
except Exception as e:
    print(e)
    pass
import datetime
from datetime import *
import time
import sys
sys.path.insert(0, '/home/wind/Renew_kutch_statistical/Renew_Statistical_model')
import Renew_Statistical_model
sys.path.insert(0, '/home/wind/Renew_kutch_statistical/renew_support')
import renew_support
sys.path.insert(0, '/home/wind/Renew_kutch/renew_id_train')
import renew_id_train
sys.path.insert(0, '/home/wind/Renew_kutch/renew_power')
import renew_power
sys.path.insert(0, '/home/wind/Renew_kutch/renew_support')
import renew_support

#turbine_model = pd.read_pickle('renew_turbinewise_forecast')
#statistical_model = pd.read_pickle('Renew_Kutch_forcast')
#actual_data = pd.read_pickle('RENEW_AGG_DATA')
turbine_model = pd.read_pickle('home/wind/Renew_kutch/renew_turbinewise_forecast')
statistical_model = pd.read_pickle('home/wind/Renew_kutch_statistical/Renew_Kutch_forcast')
actual_data = pd.read_pickle('home/wind/Renew_kutch_statistical/RENEW_AGG_DATA')
turbine_model['datetime'] = pd.to_datetime(turbine_model['datetime'])
statistical_model['datetime'] = pd.to_datetime(statistical_model['datetime'])
actual_data['datetime'] = pd.to_datetime(actual_data['datetime'])



##pulling in Rohit K's model



#models
statistical_model = statistical_model.loc[((statistical_model['datetime'] >= datetime.now() - timedelta(hours=6)) & (statistical_model['datetime'] < datetime.now())),["datetime", 'avg_power']]
turbine_model = turbine_model.loc[((turbine_model['datetime'] >= datetime.now() - timedelta(hours=6)) & (turbine_model['datetime'] < datetime.now())),["datetime", 'forecast']]
actual_data = actual_data.loc[((actual_data['datetime'] >= datetime.now() - timedelta(hours=6)) & (actual_data['datetime'] < datetime.now())),["datetime", 'power_mw']]


#pulling in actual generation value
statistical_model.rename(columns = {"avg_power": "Statistical Forecast Power"}, inplace = True)
turbine_model.rename(columns = {"forecast": "Turbine Forecast Power"}, inplace = True)
actual_data.rename(columns = {"power_mw": "Actual Generation"}, inplace = True)

#merging into single dataframe
data = pd.merge(statistical_model, turbine_model, on = ['datetime'], how = 'inner', sort=True)
comparison = pd.merge(data, actual_data, on = ['datetime'], how = 'inner', sort=True)

#calculating MAPE
comparison['statistical MAPE'] = (abs(comparison['Statistical Forecast Power']-comparison['Actual Generation'])/250)*100
comparison['turbine MAPE'] = (abs(comparison['Turbine Forecast Power']-comparison['Actual Generation'])/250)*100
#comparison['statistical MAPE'].mean()
#comparison['turbine MAPE'].mean()

#model 1 - comparing MAPE for last 6 hours
def model_1():
    if comparison['statistical MAPE'].mean() < comparison['turbine MAPE'].mean():
        print('Run Statistical Model')
        with open("Renew_Statistical_model.py") as f:
            code = compile(f.read(), "Renew_Statistical_model.py", 'exec')
            exec(code)
    if comparison['turbine MAPE'].mean() < comparison['statistical MAPE'].mean():
        print('Run Turbine Model')
        with open("renew_power.py") as f:
            code = compile(f.read(), "renew_power.py", 'exec')
            exec(code)
    if comparison['turbine MAPE'].mean() == comparison['statistical MAPE'].mean():
        print('Both equal - running Turbine Model!')
        with open("renew_power.py") as f:
            code = compile(f.read(), "renew_power.py", 'exec')
            exec(code)

#running model 1        
#model_1()
    
#model 2 - comparing error increase/decrease 
#def moving_average(a, n=len(comparison['statistical MAPE']) -2) :
 #   ret = np.cumsum(a, dtype=float)
  #  ret[n:] = ret[n:] - ret[:-n]
   # return ret[n - 1:] / n
 

            
#fit straight line to points and compare gradients of straight lines
x = np.arange(0,len(comparison['statistical MAPE']))
y=np.array(comparison['statistical MAPE'])
z_stat = np.polyfit(x,y,1)
z_stat[0] 

x = np.arange(0,len(comparison['turbine MAPE']))
y=np.array(comparison['turbine MAPE'])
z_turb = np.polyfit(x,y,1)
z_turb[0]           
            
 
#model 2 - comparing error for last 6 hours           
def model_2():
    if z_stat[0] < z_turb[0]:
        print('Run Statistical Model')
        with open("Renew_Statistical_model.py") as f:
            code = compile(f.read(), "Renew_Statistical_model.py", 'exec')
            exec(code)
    if z_turb[0] < z_stat[0]:
        print('Run Turbine Model')
        with open("renew_power.py") as f:
            code = compile(f.read(), "renew_power.py", 'exec')
            exec(code)
    if z_stat[0] == z_turb[0]:
        print('Both equal - running Turbine Model!')
        with open("renew_power.py") as f:
            code = compile(f.read(), "renew_power.py", 'exec')
            exec(code)  


#if true error is increasing, if false error is decreasing 

#res1 = np.all(np.diff(moving_average(np.array(comparison['statistical MAPE']), n=len(comparison['statistical MAPE'] )-1))>0)
# True; i.e. "generally increasing"; false 

#res2 = np.all(np.diff(moving_average(np.array(comparison['turbine MAPE']), n=len(comparison['turbine MAPE']) -1))>0)
# False, i.e. "generally not increasing"      





#model 3 - combiner model
    
