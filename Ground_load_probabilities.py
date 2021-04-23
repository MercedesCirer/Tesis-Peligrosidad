# -*- coding: utf-8 -*-
"""
Created on Thu Apr 22 10:33:44 2021

@author: Mercedes Cirer
"""
import pandas as pd
import numpy as np
import os
from netCDF4 import Dataset
from tqdm import tqdm

def lisDir(direct):
    return os.listdir(direct)

def cum(x):
    return x+1

def thresholds(dfac,dfv,th):
    dfac = cum(dfac).where(dfv > th,dfac).fillna(0.0)
    return dfac

def perc(x,n):
    return x/n*100

def export(x):    
    x.to_csv('F:/Cursos/Pandas/ground_load_TH.csv')
    #x.to_excel('F:/Cursos/Pandas/ground_load_TH.xlsx')

    
Ds= lisDir('D:/Simulaciones/')    
print(len(Ds))

loop = tqdm(total=len(Ds), position = 0, leave=False)

ths = [100,10,1]
           
for d in Ds:
    data = Dataset(r'D:/Simulaciones/{}/out_{}.part.nc'.format(d,d))
    print('Getting data from: {}'.format(d))
    
    if Ds.index(d) == 0:
        lat = data.variables['lat'][:]
        lon = data.variables['lon'][:]
        dfmax = pd.DataFrame(data = 0, index = lat, columns = lon)
        dfmed = pd.DataFrame(data = 0, index = lat, columns = lon)
        dfmin = pd.DataFrame(data = 0, index = lat, columns = lon)
        dfs = [dfmax,dfmed,dfmin]
        
    Gl=data.variables['Ground_load'][:]
    Gl=np.ma.masked_where(Gl == np.nan, Gl)
    
    dfd = pd.DataFrame(data = Gl[-1,:,:], index = lat, columns= lon).fillna(0.0)
    
    for th in ths:
        dfs[ths.index(th)] = thresholds(dfs[ths.index(th)],dfd,th)

    loop.set_description('Processing...'.format(d))
    loop.update(1)

dffs = []
i=100

for df in dfs:
    df = perc(df, len(Ds))
    serie = df.stack()    
    frame = {
        '{}'.format(str(i)): serie}    
    i=int(i/10)
    df = pd.DataFrame(frame)
    #print(df.head(5))   
    dffs.append(df)
 
dff = pd.concat(dffs, axis= 1)    
export(dff)     
loop.close()


