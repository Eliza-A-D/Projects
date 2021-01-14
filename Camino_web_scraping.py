# -*- coding: utf-8 -*-
"""
Created on Thu Jan 14 18:22:27 2021

@author: eliza
"""
from requests import get
from bs4 import BeautifulSoup
import pandas as pd
url = 'https://vivecamino.com/en/the-camino-de-santiago-in-2019:-records,-routes,-pilgrims-all-you-need-to-know-no-554/'   
response = get(url)    
html_soup = BeautifulSoup(response.text, 'html.parser')
#type(html_soup)
#getting data
whole_data_ = html_soup.find_all('div', class_ = "ct")   


whole_data_ = whole_data_.find_all('ul') 


result = []
for th in whole_data_:
        result.extend(th.find_all("ul"))
        
res = result[1]

res_text = res.text

Month = ['Jan 19', 'Feb 19'] #, 'Mar 19', 'Apr 19', 'May 19', 'Jun 19', 'Jul 19', 'Aug 19', 'Sep 19', 'Oct 19', 'Nov 19', 'Dec 19']
Hikers = [res.text[10:15].replace(".",""), res.text[56:61].replace(".","")]

#storing result in pandas dataframe
df = pd.DataFrame(list(zip(Month, Hikers)), columns =['Month', 'Hikers'])




    
    
    
    
    
