# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 13:51:04 2020

aerosol and gasses correlations

@author: white
"""

import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 22})
import pandas as pd
import scipy.signal as ss
from scipy.optimize import curve_fit
from datetime import datetime


lod = 2
S = 0

now = datetime.now()

current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)



#%%

fa = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\aerosol_data\aerosol_data.xlsx',
                   sheet_name='Sheet1')

print('aerosols read-in finished.')


# TIMEa = fa['TIME']
TIMEaN = fa['TimeN']
CP = fa['CONC_CP']
trace_0_3µm = fa['CONC_0U3']
trace_0_5µm = fa['CONC_0U5']
trace_0_7µm = fa['CONC_0U7']
trace_1_0µm = fa['CONC_1U0']
trace_2_5µm = fa['CONC_2U5']
trace_5_0µm = fa['CONC_5U0']
TSP = fa['TSP_MASS']
BC = fa['BC_MASS']

aerosol_labels = ['CP', '0_3µm', '0_5µm', '0_7µm', '1_0µm', '2_5µm', '5_0µm', 'TSP', 'BC']
aerosols = [CP, trace_0_3µm, trace_0_5µm,
            trace_0_7µm, trace_1_0µm, trace_2_5µm,
            trace_5_0µm, TSP, BC]

#%%

fg = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\gasses_data\gasses_data.xlsx',
                   sheet_name='Sheet1')

print('gasses read-in finished.')

# TIMEg = fg['Timestamp [MEZ]']
TIMEgN = fg['TimeN']
CO2 = np.where( fg['EU1(CO2:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CO2:SON1:10[ppm])'] )
CH4 = np.where( fg['EU1(CH4_THG:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CH4_THG:SON1:10[ppm])'] )
NO = np.where( fg['EU1(NO:SON1:10[ppb])'] == -99, np.nan, fg['EU1(NO:SON1:10[ppb])'] )
NO2 = np.where( fg['EU1(NO2#2:SON1:10[ppb])'] == -99, np.nan, fg['EU1(NO2#2:SON1:10[ppb])'] )
O3 = np.where( fg['EU1(O3:SON1:10[ppb])'] == -99, np.nan, fg['EU1(O3:SON1:10[ppb])'] )
CO = np.where( fg['EU1(CO:SON1:10[ppm])'] == -99, np.nan, fg['EU1(CO:SON1:10[ppm])'] )
SO2 = np.where( fg['EU1(SO2:SON1:10[ug/m3])'] == -99, np.nan, fg['EU1(SO2:SON1:10[ug/m3])'] )

gasses_labels = ['CO2', 'CH4', 'NO', 'NO2', 'O3', 'CO', 'SO2']
gasses = [CO2, CH4, NO, NO2, O3, CO, SO2]


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


Time = np.append(f['TIME'], f2['TIME'])

TimeN = np.append(f[' JulianDate'], f2[' JulianDate'])
TimeN += 39814

############################
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)
############################



#%%

Section_s = [slice(0, 35861), slice(37972, 71284), slice(76747, None)] # PTR data
Section_a = [slice(80, 262), slice(1320, 1474), slice(3180, 3348)] # aerosol and gas data
Season = ['Summer', 'Autum', 'Winter']
Days = ['Aug. 04 - 11', 'Sep. 25 - Oct. 01', 'Dec. 11 - 18']

# 1st half masses = 6:167
# 2nd half masses = 167:
masses = f.columns[6:]

#%%

def base_line(x, b):
    return b

def reject_outliers(data, data2, m = 6.):
    data = np.asarray(data)
    data2 = np.asarray(data2)
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    data = data[s<m]
    data2 = data2[s<m]
    data = list(data)
    data2 = list(data2)
    return data, data2




#%%

for S in range(3):
    print('starting {}'.format(Season[S]))
    
    time = Time[Section_s[S]]
    timeN = TimeN[Section_s[S]]
    Ind = np.append( f[' indM'], f2[' indM'] )
    ind = Ind[Section_s[S]]
    
    STRT = TimeN[Section_s[S]][0]
    STP = TimeN[Section_s[S]][-1]
    theTIMEaxis = np.linspace(STRT, STP, time.size)
    
    df_corr_ALL = pd.DataFrame()
    
    for M in range(masses.size):
        # M = 69
        
        MASS = masses[M]
        print('calc for {} (index {})'.format(MASS, M))
        
        ###############################################
        # Base Signal Average
        Raw = np.append( f[MASS], f2[MASS] )
        signal = Raw[Section_s[S]]
        ## split into base and signal
        base = np.where(ind == 100, signal, np.nan)
        signal = np.where(ind == 300, signal, np.nan)
        
        
        ## convert base into x y data leaving out nans
        xbase = []
        ybase = []
        for i in range(base.size):
            if base[i] > 0:
                xbase.append(timeN[i])
                ybase.append(base[i])
        
        ## reject outliers in baseline
        ybase, xbase = reject_outliers(ybase, xbase)
        ## linear fit for baseline
        popt, pcov = curve_fit(base_line, xbase, ybase)
        
        ybase_arr = np.asarray(ybase)
        
        Stdv = np.std(ybase_arr)
        LOD = lod*Stdv
        
        ## generate baseline and LODline
        base_fit = np.zeros(len(ybase))
        LODline = np.zeros(len(ybase))
        for i in range(len(ybase)):
            base_fit[i] = base_line(xbase[i], popt[0])
            LODline[i] = LOD
        
        
        
        
        # example plot
        
        # plt.plot(xbase, ybase, label='background signal')
        # plt.plot(timeN, signal, label='signal')
        
        smooth = ss.medfilt(signal, kernel_size=1441)
        smooth = ss.medfilt(smooth, kernel_size=1441)
        
        ## convert signal to x y data and leave out anything below LOD
        # x_sig = []
        # y_sig = []
        # for i in range(signal.size):
        #     if signal[i] > LOD[0]:
        #         x_sig.append(timeN[i])
        #         y_sig.append(signal[i])
        
        
        interp_signal = np.interp(theTIMEaxis, timeN, smooth)
        interp_signal_sub = interp_signal - base_fit[0]
        
        if S == 0:
            interp_signal_sub[6090:9408] = np.nan
        
        # plt.plot(interp_signal, label='interp')
        
        #
        interp_signal_sub[~np.isnan(interp_signal_sub)] = np.where(interp_signal_sub[~np.isnan(interp_signal_sub)] > LOD,
                                     interp_signal_sub[~np.isnan(interp_signal_sub)],  0)
        
        throw_out = np.median(interp_signal_sub[~np.isnan(interp_signal_sub)])
        
        if throw_out == 0:
            interp_signal_sub[:] = 0
            print('weak signal')
        

        interp_signal_sub[~np.isnan(interp_signal_sub)] = np.where(interp_signal_sub[~np.isnan(interp_signal_sub)] > LOD,
                                     interp_signal_sub[~np.isnan(interp_signal_sub)],  np.nan)
        
    #%%
        
        time_aN = TIMEaN[Section_a[S]]
        time_aN = np.asarray(time_aN)
        
        interpAerosols = []
        for i in range(len(aerosols)):
            trace = aerosols[i][Section_a[S]]
            # trace = np.where( trace > 0, trace, np.nan )
            interpTrace = np.interp(theTIMEaxis, time_aN, trace)
            interpAerosols.append(interpTrace)
        
        interpGasses = []
        for i in range(len(gasses)):
            trace = gasses[i][Section_a[S]]
            # trace = np.where( trace > 0, trace, np.nan )
            interpTrace = np.interp(theTIMEaxis, time_aN, trace)
            interpGasses.append(interpTrace)
        
    
        Summer_data = { '{}'.format(MASS):interp_signal_sub,
                       aerosol_labels[0]:interpAerosols[0],
                       aerosol_labels[1]:interpAerosols[1],
                       aerosol_labels[2]:interpAerosols[2],
                       aerosol_labels[3]:interpAerosols[3],
                       aerosol_labels[4]:interpAerosols[4],
                       aerosol_labels[5]:interpAerosols[5],
                       aerosol_labels[6]:interpAerosols[6],
                       aerosol_labels[7]:interpAerosols[7],
                       aerosol_labels[8]:interpAerosols[8],
                       gasses_labels[0]:interpGasses[0],
                       gasses_labels[1]:interpGasses[1],
                       gasses_labels[2]:interpGasses[2],
                       gasses_labels[3]:interpGasses[3],
                       gasses_labels[4]:interpGasses[4],
                       gasses_labels[5]:interpGasses[5],
                       gasses_labels[6]:interpGasses[6],
            }
        
        
        df_interps = pd.DataFrame(Summer_data)
        corr = df_interps.corr()
        
        df_corr_ALL[corr.columns[0]] = corr[corr.columns[0]][1:]
    
    
    
    df_corr_ALL.to_excel(r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\aerosol_data\{}_corr_LOD{}_smoothLOD2.xlsx'.format(Season[S], lod))
    print('spreadsheet saved.')

print('program finished')

#%%
# # plt.plot(timeN_rej, sig_rej, label='signal_rej')
# plt.plot(xbase, ybase, label='background signal', alpha=0.5)

# plt.plot(timeN, signal, label='signal', color='black', alpha=0.3)

# plt.plot(xbase, base_fit, label='background fit = {:.4f} ppb'.format(popt[0]), color='purple', linewidth=3)
# plt.plot(xbase, LODline, 'r--', label='LOD={:.4f}({}σ)'.format(LOD,lod), linewidth=3)
# plt.plot(theTIMEaxis, interp_signal_sub, label='subtracted smooth signal', color='green')
# # plt.plot(theTIMEaxis, interpGasses[5])
# # plt.plot(timeN, smooth, label='smooth')

# plt.title('{} m/z'.format(MASS))
# plt.xlabel('Julian time')
# plt.ylabel('ppb')    
# plt.legend()

