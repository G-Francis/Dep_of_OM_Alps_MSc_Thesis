# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:51:04 2020

PTR-MS data, Gasses data, and Meteorological data reader
as part of Master Thesis: Deposition of Organic Matter on Alpine Snow

@author: Grant Francis
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import pandas as pd




#%%

fg = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\gasses_data\gasses_data.xlsx',
                   sheet_name='Sheet1')

print('gasses read-in finished.')

TIMEg = fg['Timestamp [MEZ]']
# TIMEg = np.where( fg['Timestamp [MEZ]'] == -99, np.nan, fg['Timestamp [MEZ]'] )
CO2 = np.where( fg['EU1(CO2:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CO2:SON1:10[ppm])'] )
CH4 = np.where( fg['EU1(CH4_THG:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CH4_THG:SON1:10[ppm])'] )
NO = np.where( fg['EU1(NO:SON1:10[ppb])'] == -99, np.nan, fg['EU1(NO:SON1:10[ppb])'] )
NO2 = np.where( fg['EU1(NO2#2:SON1:10[ppb])'] == -99, np.nan, fg['EU1(NO2#2:SON1:10[ppb])'] )
O3 = np.where( fg['EU1(O3:SON1:10[ppb])'] == -99, np.nan, fg['EU1(O3:SON1:10[ppb])'] )
CO = np.where( fg['EU1(CO:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CO:SON1:10[ppm])'] )
SO2 = np.where( fg['EU1(SO2:SON1:10[ug/m3])'] == -99, np.nan, fg['EU1(SO2:SON1:10[ug/m3])'] )


#%% read in file
print('reading in 1st file PTR data...')

f = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\PTR_live\FIRSThalf_test.xlsx',
                   sheet_name='Sheet1')

print('read-in finished.')


# read in file
print('reading in 2nd file PTR data...')

f2 = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\PTR_live\SECONDhalf_test.xlsx',
                   sheet_name='Sheet1')

print('read-in finished.')


masses = f.columns[6:]


#%%
Section_s = [slice(0, 35862), slice(37972, 71284), slice(76747, None)] # PTR data
Section_a = [slice(80, 262), slice(1320, 1474), slice(3180, 3348)]
Season = ['Summer', 'Autum', 'Winter']
Days = ['Aug. 04 - 11', 'Sep. 25 - Oct. 01', 'Dec. 11 - 18']


indM = np.append(f[' indM'], f2[' indM'])
TIME = np.append(f['TIME'], f2['TIME'])

#%%
met_data = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\met_data\SBO_Met_201908-201912.xlsx', sheet_name='Sheet1')



#%%

time = met_data['DATUM']
temp = met_data['temp']
dtemp = met_data['dewpt temp']
direction = met_data['direction']
speed = met_data['speed']
hum = met_data['% humidity']

#%%
time = time.mask(time=='---')
temp = temp.mask(temp=='---')
dtemp = dtemp.mask(dtemp=='---')
direction = direction.mask(direction=='---')
speed = speed.mask(speed=='---',0)
hum = hum.mask(hum=='---')

speed = speed.to_numpy()
speed = speed.astype(int)


#%%


for M in range(1): # Starting with acetonitrile
    
    MASS = masses[M]
    M_ace = MASS
    
    print('starting {} (indx: {}).'.format(MASS, M))
    
    # Base Signal Average 1
    
    base = np.where(f[' indM'] == 100, f[MASS], 0)
    avgs = np.zeros(base.size)
    
    group = []
    inds = []
    cnt0 = 0
    for i in range(base.size):
        
        if f[' indM'][i] == 100:
            cnt0 = 0
            group.append(base[i])
            inds.append(i)
        
        if f[' indM'][i] == 300 and cnt0 == 0:
            cnt0 += 1
            if len(group) > 0:
                avg = np.average(group)
                # save in avgs
                avgs[inds] = avg
            # reset
            group = []
            inds = []
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(avgs[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(avgs[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group) > 0:
                avgs[inds1[-1]+1:inds2[0]] = np.average(group)
            # reset and backtrack
            i = inds1[-1]
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 1
    
    STDV = np.zeros(base.size)
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(base[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(base[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            if len(group) > 0:
                # save in STDV
                STDV[inds1[-1]:inds2[0]] = np.std(group)
            # reset and backtrack
            i = inds1[-1] + 1
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
    
    
    # Base Signal Average 2
    
    base2 = np.where(f2[' indM'] == 100, f2[MASS], 0)
    avgs2 = np.zeros(base2.size)
    
    group2 = []
    inds2 = []
    cnt02 = 0
    for i in range(base2.size):
        
        if f2[' indM'][i] == 100:
            cnt02 = 0
            group2.append(base2[i])
            inds2.append(i)
        
        if f2[' indM'][i] == 300 and cnt02 == 0:
            cnt02 += 1
            if len(group2) >0:
                avg2 = np.average(group2)
                # save in avgs
                avgs2[inds2] = avg2
            # reset
            group2 = []
            inds2 = []
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(avgs2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(avgs2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group2) > 0:
                avgs2[inds12[-1]+1:inds22[0]] = np.average(group2)
            # reset and backtrack
            i = inds12[-1]
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 2
    
    STDV2 = np.zeros(base2.size)
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(base2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(base2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # save in STDV
            if len(group2) > 0:
                STDV2[inds12[-1]:inds22[0]] = np.std(group2)
            # reset and backtrack
            i = inds12[-1] + 1
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
    
    
    # Sutbtract average base and create LOD
    Signal = f[MASS]
    Signal = Signal.append(f2[MASS])
    
    avgs = np.append(avgs, avgs2)
    
    Subtracted = Signal - avgs
    
    Subtracted = np.where(Subtracted > 0, Subtracted, 0)
    scale_ace = Subtracted
    STDV = np.append(STDV, STDV2)
    
    LOD3 = STDV*3
    

Y_ace = np.where( Subtracted > LOD3, Subtracted, np.nan)
Y_ace = np.where( indM == 300, Y_ace, np.nan)


for M in range(4,5): # benzene
    
    MASS = masses[M]
    M_ben = MASS
    
    print('starting {} (indx: {}).'.format(MASS, M))
    
    # Base Signal Average 1
    
    base = np.where(f[' indM'] == 100, f[MASS], 0)
    avgs = np.zeros(base.size)
    
    group = []
    inds = []
    cnt0 = 0
    for i in range(base.size):
        
        if f[' indM'][i] == 100:
            cnt0 = 0
            group.append(base[i])
            inds.append(i)
        
        if f[' indM'][i] == 300 and cnt0 == 0:
            cnt0 += 1
            if len(group) > 0:
                avg = np.average(group)
                # save in avgs
                avgs[inds] = avg
            # reset
            group = []
            inds = []
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(avgs[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(avgs[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group) > 0:
                avgs[inds1[-1]+1:inds2[0]] = np.average(group)
            # reset and backtrack
            i = inds1[-1]
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 1
    
    STDV = np.zeros(base.size)
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(base[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(base[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            if len(group) > 0:
                # save in STDV
                STDV[inds1[-1]:inds2[0]] = np.std(group)
            # reset and backtrack
            i = inds1[-1] + 1
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
    
    
    # Base Signal Average 2
    
    base2 = np.where(f2[' indM'] == 100, f2[MASS], 0)
    avgs2 = np.zeros(base2.size)
    
    group2 = []
    inds2 = []
    cnt02 = 0
    for i in range(base2.size):
        
        if f2[' indM'][i] == 100:
            cnt02 = 0
            group2.append(base2[i])
            inds2.append(i)
        
        if f2[' indM'][i] == 300 and cnt02 == 0:
            cnt02 += 1
            if len(group2) >0:
                avg2 = np.average(group2)
                # save in avgs
                avgs2[inds2] = avg2
            # reset
            group2 = []
            inds2 = []
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(avgs2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(avgs2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group2) > 0:
                avgs2[inds12[-1]+1:inds22[0]] = np.average(group2)
            # reset and backtrack
            i = inds12[-1]
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 2
    
    STDV2 = np.zeros(base2.size)
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(base2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(base2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # save in STDV
            if len(group2) > 0:
                STDV2[inds12[-1]:inds22[0]] = np.std(group2)
            # reset and backtrack
            i = inds12[-1] + 1
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
    
    
    # Sutbtract average base and create LOD
    Signal = f[MASS]
    Signal = Signal.append(f2[MASS])
    
    avgs = np.append(avgs, avgs2)
    
    Subtracted = Signal - avgs
    
    Subtracted = np.where(Subtracted > 0, Subtracted, 0)
    scale_ben = Subtracted
    STDV = np.append(STDV, STDV2)
    
    LOD3 = STDV*3
    

Y_ben = np.where( Subtracted > LOD3, Subtracted, np.nan)
Y_ben = np.where( indM == 300, Y_ben, np.nan)



for M in range(6,7): # toluene
    
    MASS = masses[M]
    M_tol = MASS
    
    print('starting {} (indx: {}).'.format(MASS, M))
    
    # Base Signal Average 1
    
    base = np.where(f[' indM'] == 100, f[MASS], 0)
    avgs = np.zeros(base.size)
    
    group = []
    inds = []
    cnt0 = 0
    for i in range(base.size):
        
        if f[' indM'][i] == 100:
            cnt0 = 0
            group.append(base[i])
            inds.append(i)
        
        if f[' indM'][i] == 300 and cnt0 == 0:
            cnt0 += 1
            if len(group) > 0:
                avg = np.average(group)
                # save in avgs
                avgs[inds] = avg
            # reset
            group = []
            inds = []
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(avgs[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(avgs[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group) > 0:
                avgs[inds1[-1]+1:inds2[0]] = np.average(group)
            # reset and backtrack
            i = inds1[-1]
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 1
    
    STDV = np.zeros(base.size)
    
    group = []
    inds1 = []
    inds2 = []
    half = 0
    cnt0 = 0
    reset = 1
    i = 0
    while i < base.size:
        
        if (f[' indM'][i] == 100) and (half == 0):
            group.append(base[i])
            inds1.append(i)
            cnt0 = 0
            reset = 0
            # print('first')
        
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 0) and (reset == 0):
            half = 1
            cnt0 = 1
            # print('half switch')
            
        if (f[' indM'][i] == 100) and (half == 1):
            group.append(base[i])
            inds2.append(i)
            cnt0 = 0
            # print('second')
    
        if (f[' indM'][i] == 300) and (cnt0 == 0) and (half == 1):
            if len(group) > 0:
                # save in STDV
                STDV[inds1[-1]:inds2[0]] = np.std(group)
            # reset and backtrack
            i = inds1[-1] + 1
            group = []
            inds1 = []
            inds2 = []
            cnt0 = 0
            half = 0
            reset = 1
            # print('reset')
        i += 1
    
    
    # Base Signal Average 2
    
    base2 = np.where(f2[' indM'] == 100, f2[MASS], 0)
    avgs2 = np.zeros(base2.size)
    
    group2 = []
    inds2 = []
    cnt02 = 0
    for i in range(base2.size):
        
        if f2[' indM'][i] == 100:
            cnt02 = 0
            group2.append(base2[i])
            inds2.append(i)
        
        if f2[' indM'][i] == 300 and cnt02 == 0:
            cnt02 += 1
            if len(group2) >0:
                avg2 = np.average(group2)
                # save in avgs
                avgs2[inds2] = avg2
            # reset
            group2 = []
            inds2 = []
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(avgs2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(avgs2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # fill in avgs ind 300 with surrounding avgs in 100
            if len(group2) > 0:
                avgs2[inds12[-1]+1:inds22[0]] = np.average(group2)
            # reset and backtrack
            i = inds12[-1]
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
        
    
    # Base Signal STDV 2
    
    STDV2 = np.zeros(base2.size)
    
    group2 = []
    inds12 = []
    inds22 = []
    half2 = 0
    cnt02 = 0
    reset2 = 1
    i = 0
    while i < base2.size:
        
        if (f2[' indM'][i] == 100) and (half2 == 0):
            group2.append(base2[i])
            inds12.append(i)
            cnt02 = 0
            reset2 = 0
            # print('first')
        
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 0) and (reset2 == 0):
            half2 = 1
            cnt02 = 1
            # print('half switch')
            
        if (f2[' indM'][i] == 100) and (half2 == 1):
            group2.append(base2[i])
            inds22.append(i)
            cnt02 = 0
            # print('second')
    
        if (f2[' indM'][i] == 300) and (cnt02 == 0) and (half2 == 1):
            # save in STDV
            if len(group2) > 0:
                STDV2[inds12[-1]:inds22[0]] = np.std(group2)
            # reset and backtrack
            i = inds12[-1] + 1
            group2 = []
            inds12 = []
            inds22 = []
            cnt02 = 0
            half2 = 0
            reset2 = 1
            # print('reset')
        i += 1
    
    
    # Sutbtract average base and create LOD
    Signal = f[MASS]
    Signal = Signal.append(f2[MASS])
    
    avgs = np.append(avgs, avgs2)
    
    Subtracted = Signal - avgs
    
    Subtracted = np.where(Subtracted > 0, Subtracted, 0)
    scale_tol = Subtracted
    STDV = np.append(STDV, STDV2)
    
    LOD3 = STDV*3
    

Y_tol = np.where( Subtracted > LOD3, Subtracted, np.nan)
Y_tol = np.where( indM == 300, Y_tol, np.nan)

    
#%%
    
i = 0
for i in range(2, 3):  

    plt.figure(figsize=(40,21))

    T = TIMEg[Section_a[i]]
    
    
    ax1 = plt.subplot(5, 1, 1)
    sc = plt.scatter(time, direction, c=speed, label='wind direction', cmap='inferno')
    plt.axvline(x=pd.Timestamp('2019-12-14 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-16 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-18 12:00:00'), color='black')
    plt.xticks(size=25)
    ax1.set_ylabel('Wind Direction [°]', size=25)
    ax1.text(0.01, 0.5, 'N    E    S    W    N',
            horizontalalignment='center',
            verticalalignment='center',
            rotation='vertical',
            transform=ax1.transAxes)
    plt.colorbar(sc, extend='both', label='Wind Speed [m/s]', fraction=0.01, pad=-0.02)
    
    
    ax1 = plt.subplot(5, 1, 2)################################################################
    lns1 = plt.plot(T, CO2[Section_a[i]], label='CO$_2$', color='black', linewidth=3)
    plt.axvline(x=pd.Timestamp('2019-12-14 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-16 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-18 12:00:00'), color='black')
    plt.ylabel('CO$_2$ [ppm]', size=30) #, labelpad=-2220)
    ax2 = ax1.twinx()
    lns2 = ax2.plot(T, CO[Section_a[i]], label='CO', color='violet', linewidth=3)
    ax2.set_ylabel('CO [ppm]', size=30)


    lns = lns1 + lns2
    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper right', fontsize=30)


    plt.subplot(5, 1, 3)
    plt.scatter(TIME[Section_s[i]], Y_tol[Section_s[i]], s=1, c='brown', alpha=0.7, label='Toluene {}$m/z$'.format(M_tol))
    plt.axvline(x=pd.Timestamp('2019-12-14 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-16 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-18 12:00:00'), color='black')


    scale = 2.5*np.percentile(scale_tol[Section_s[i]], 90)
    if scale == 0:
        scale = 2.5*np.max(scale_tol[Section_s[i]])
    plt.ylim(0, scale)
    plt.legend(loc='upper right', markerscale=10, fontsize=30) #, handlelength=0
    plt.ylabel('[ppb]', fontsize=30)
    
    
    ###############################################################################################
    plt.subplot(5, 1, 4)
    plt.scatter(TIME[Section_s[i]], Y_ben[Section_s[i]], s=1, c='darkgreen', alpha=0.7, label='Benzene {}$m/z$'.format(M_ben))
    plt.axvline(x=pd.Timestamp('2019-12-14 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-16 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-18 12:00:00'), color='black')
    # plt.plot(time[Section_s[i]], smooth[Section_s[i]], color='purple', label='Median', linewidth=3)
    scale = 2.5*np.percentile(scale_ben[Section_s[i]], 90)
    if scale == 0:
        scale = 2.5*np.max(scale_ben[Section_s[i]])
    plt.ylim(0, scale)
    plt.legend(loc='upper right', markerscale=10, fontsize=30) #, handlelength=0
    plt.ylabel('[ppb]', size=30)
    
    
    ###############################################################################################
    plt.subplot(5, 1, 5)
    plt.scatter(TIME[Section_s[i]], Y_ace[Section_s[i]], s=1, c='orange', alpha=0.7, label='Acetonitrile {}$m/z$'.format(M_ace))
    plt.axvline(x=pd.Timestamp('2019-12-14 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-16 12:00:00'), color='black')
    plt.axvline(x=pd.Timestamp('2019-12-18 12:00:00'), color='black')
    scale = 2.5*np.percentile(scale_ace[Section_s[i]], 90)
    if scale == 0:
        scale = 2.5*np.max(scale_ace[Section_s[i]])
    plt.ylim(0, scale)
    plt.ylabel('[ppb]', size=30)
    plt.xlabel('Date [YYYY-MM-DD]', size=30)
    plt.legend(loc='upper right', markerscale=10, fontsize=30)#!!! bbox_to_anchor=(1, 0.5), 

    # plt.savefig('{}_gasses_{}.png'.format(MASS, Season[i])) #, bbox_inches='tight')
    # plt.close()
   
