# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 12:30:19 2020

Snow individual timelines

@author: white
"""


import numpy as np
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 30})
import pandas as pd
import statistics as stat


#%%
print('reading in data')
## filtered
Fsmpls = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\reassessed_2.5_10min_0_213.xlsx', sheet_name='Fsmpls')
Fblnks = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\reassessed_2.5_10min_0_213.xlsx', sheet_name='Fblnks')

## non-filtered
smpls = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\reassessed_2.5_10min_0_213.xlsx', sheet_name='smpls')
blnks = pd.read_excel (r'C:\Users\white\Documents\Utrecht\PTR_MS\Sonnblick\reassessed_2.5_10min_0_213.xlsx', sheet_name='blnks')


#%% remove non-organic mass signals below 40 Da
## keep these:
## mass[16] = 31.018
## mass[19] = 33.033
## mass[26] = 40.026 and above

_drop_masses = ['START (FULL)', 'STRT (Daily)',  'tSTRTav',  ' tENDav',
               ' JulianDate',  14.002,  14.014,  15.022,  15.993,  17.026,
               18.034,  19.013,  20.023,  21.022,  26.015,  27.022,  28.004,
               28.017,  29.013,  29.997,  30.995,  31.984,  32.994,  33.992,
               35.037,  36.022, 37.026,  38.034, 39.032]

Fsmpls = Fsmpls.drop(_drop_masses, axis=1)
Fblnks = Fblnks.drop(_drop_masses, axis=1)
smpls = smpls.drop(_drop_masses, axis=1)
blnks = blnks.drop(_drop_masses, axis=1)


#%% Blanks

blnk_avg = blnks[:18].mean()
# blnks_avg = blnks.iloc[19,:]
blnk_LOD = np.std( blnks[:18] ) * 3

Fblnk_avg = Fblnks[:18].mean()
# Fblnks_avg = Fblnks.iloc[19,:]
Fblnk_LOD = np.std( Fblnks[:18] ) * 3

#%%

_Dec14 = [[],[],[],[],[],[],[],[],[],[]]
_Dec16 = [[],[],[],[],[],[],[],[],[],[]]
_Dec18 = [[],[],[],[],[],[],[],[],[],[]]

_DEC14 = [[],[],[],[],[],[],[],[],[],[]]
_DEC16 = [[],[],[],[],[],[],[],[],[],[]]
_DEC18 = [[],[],[],[],[],[],[],[],[],[]]

_Dec14F = [[],[],[],[],[],[],[],[],[],[]]
_Dec16F = [[],[],[],[],[],[],[],[],[],[]]
_Dec18F = [[],[],[],[],[],[],[],[],[],[]]

_DEC14F = [[],[],[],[],[],[],[],[],[],[]]
_DEC16F = [[],[],[],[],[],[],[],[],[],[]]
_DEC18F = [[],[],[],[],[],[],[],[],[],[]]


_Dec14std = [[],[],[],[],[],[],[],[],[],[]]
_Dec16std = [[],[],[],[],[],[],[],[],[],[]]
_Dec18std = [[],[],[],[],[],[],[],[],[],[]]

_Dec14Fstd = [[],[],[],[],[],[],[],[],[],[]]
_Dec16Fstd = [[],[],[],[],[],[],[],[],[],[]]
_Dec18Fstd = [[],[],[],[],[],[],[],[],[],[]]


#%% Samples averaged across replicates

smpl_list1 = [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, '1.8a', '1.8b', 1.9]
Fsmpl_list1 = ['1.1F', '1.2F', '1.3F', '1.4F', '1.5F', '1.6F', '1.7F', '1.8aF', '1.8bF', '1.9F']

smpl_list3 = [3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7, '3.8a', '3.8b', 3.9]
Fsmpl_list3 = ['3.1F', '3.2F', '3.3F', '3.4F', '3.5F', '3.6F', '3.7F', '3.8aF', '3.8bF', '3.9F']

smpl_list5 = [5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, '5.8a', '5.8b', 5.9]
Fsmpl_list5 = ['5.1F', '5.2F', '5.3F', '5.4F', '5.5F', '5.6F', '5.7F', '5.8aF', '5.8bF', '5.9F']



for i in range(len(smpl_list1)):

    _Dec14[i] = smpls[smpls['SAMPLE']==smpl_list1[i]]
    _Dec14std[i] = np.std(_Dec14[i])
    _DEC14[i] = _Dec14[i].mean()
    if (i < 7 or i > 8):
        _Dec14std[i] = _Dec14std[i][1:]
        _DEC14[i] = _DEC14[i][1:]
        
    _Dec14F[i] = Fsmpls[Fsmpls['SAMPLE']==Fsmpl_list1[i]]
    _Dec14Fstd[i] = np.std(_Dec14F[i])
    _DEC14F[i] = _Dec14F[i].mean()


    _Dec16[i] = smpls[smpls['SAMPLE']==smpl_list3[i]]
    _Dec16std[i] = np.std(_Dec16[i])
    _DEC16[i] = _Dec16[i].mean()
    if (i < 7 or i > 8):    
        _Dec16std[i] = _Dec16std[i][1:]
        _DEC16[i] = _DEC16[i][1:]
    
    _Dec16F[i] = Fsmpls[Fsmpls['SAMPLE']==Fsmpl_list3[i]]
    _Dec16Fstd[i] = np.std(_Dec16F[i])
    _DEC16F[i] = _Dec16F[i].mean()
    
    
    _Dec18[i] = smpls[smpls['SAMPLE']==smpl_list5[i]]
    _Dec18std[i] = np.std(_Dec18[i])
    _DEC18[i] = _Dec18[i].mean()
    if (i < 7 or i > 8):
        _Dec18std[i] = _Dec18std[i][1:]
        _DEC18[i] = _DEC18[i][1:]
    
    _Dec18F[i] = Fsmpls[Fsmpls['SAMPLE']==Fsmpl_list5[i]]
    _Dec18Fstd[i] = np.std(_Dec18F[i])
    _DEC18F[i] = _Dec18F[i].mean()

#%%
## missing location on Dec 16th
_DEC16[1][:] = 0
_DEC16F[1][:] = 0
_DEC16[1] = _DEC16[1][2:]
_DEC16F[1] = _DEC16F[1][3:]

_Dec16std[1][:] = 0
_Dec16Fstd[1][:] = 0
_Dec16std[1] = _Dec16std[1][2:]
_Dec16Fstd[1] = _Dec16Fstd[1][3:]

#%% Blank subtraction

DEC14_sub = [[],[],[],[],[],[],[],[],[],[]]
DEC16_sub = [[],[],[],[],[],[],[],[],[],[]]
DEC18_sub = [[],[],[],[],[],[],[],[],[],[]]

DEC14F_sub = [[],[],[],[],[],[],[],[],[],[]]
DEC16F_sub = [[],[],[],[],[],[],[],[],[],[]]
DEC18F_sub = [[],[],[],[],[],[],[],[],[],[]]



for i in range(len(smpl_list1)):
    
    DEC14_sub[i] = _DEC14[i] - blnk_avg
    DEC16_sub[i] = _DEC16[i] - blnk_avg
    DEC18_sub[i] = _DEC18[i] - blnk_avg

    DEC14F_sub[i] = _DEC14F[i] - Fblnk_avg
    DEC16F_sub[i] = _DEC16F[i] - Fblnk_avg
    DEC18F_sub[i] = _DEC18F[i] - Fblnk_avg
    

#%% Plots (before subtration)

# plt.figure()
# plt.bar(np.arange(402), DEC14_sub[0], yerr=_Dec14std[0])
# plt.plot(np.arange(402), blnk_LOD, 'r--')
# plt.xticks(np.arange(402), DEC14_sub[0].index)



#%% Zero everything below LOD

DEC14_sub_z = [[],[],[],[],[],[],[],[],[],[]]
DEC16_sub_z = [[],[],[],[],[],[],[],[],[],[]]
DEC18_sub_z = [[],[],[],[],[],[],[],[],[],[]]

DEC14F_sub_z = [[],[],[],[],[],[],[],[],[],[]]
DEC16F_sub_z = [[],[],[],[],[],[],[],[],[],[]]
DEC18F_sub_z = [[],[],[],[],[],[],[],[],[],[]]

_Dec14std_z = [[],[],[],[],[],[],[],[],[],[]]
_Dec16std_z = [[],[],[],[],[],[],[],[],[],[]]
_Dec18std_z = [[],[],[],[],[],[],[],[],[],[]]

_Dec14Fstd_z = [[],[],[],[],[],[],[],[],[],[]]
_Dec16Fstd_z = [[],[],[],[],[],[],[],[],[],[]]
_Dec18Fstd_z = [[],[],[],[],[],[],[],[],[],[]]


for i in range(len(smpl_list1)):
    DEC14_sub_z[i] = np.where(DEC14_sub[i] > blnk_LOD, DEC14_sub[i], 0)
    _Dec14std_z[i] = np.where(DEC14_sub_z[i] > 0, _Dec14std[i], 0)
    
    DEC16_sub_z[i] = np.where(DEC16_sub[i] > blnk_LOD, DEC16_sub[i], 0)
    _Dec16std_z[i] = np.where(DEC16_sub_z[i] > 0, _Dec16std[i], 0)
    
    DEC18_sub_z[i] = np.where(DEC18_sub[i] > blnk_LOD, DEC18_sub[i], 0)
    _Dec18std_z[i] = np.where(DEC18_sub_z[i] > 0, _Dec18std[i], 0)
    
    DEC14F_sub_z[i] = np.where(DEC14F_sub[i] > Fblnk_LOD, DEC14F_sub[i], 0)
    _Dec14Fstd_z[i] = np.where(DEC14F_sub_z[i] > 0, _Dec14Fstd[i], 0)
    
    DEC16F_sub_z[i] = np.where(DEC16F_sub[i] > Fblnk_LOD, DEC16F_sub[i], 0)
    _Dec16Fstd_z[i] = np.where(DEC16F_sub_z[i] > 0, _Dec16Fstd[i], 0)
    
    DEC18F_sub_z[i] = np.where(DEC18F_sub[i] > Fblnk_LOD, DEC18F_sub[i], 0)
    _Dec18Fstd_z[i] = np.where(DEC18F_sub_z[i] > 0, _Dec18Fstd[i], 0)

    

#%% Totals Plots by mass

# _cutoff_Da = 0 # cutoff mass in [Da]

for m in range(DEC14_sub[0].index.size):
# for m in range(125,126):
    
    MASS = DEC14_sub[0].index[m]
    
    ## convert to ng/ml
    for i in range(len(smpl_list1)):
        DEC14_sub_z[i][m] = DEC14_sub_z[i][m]*MASS*0.02233
        _Dec14std_z[i][m] = _Dec14std_z[i][m]*MASS*0.02233
        
        DEC16_sub_z[i][m] = DEC16_sub_z[i][m]*MASS*0.02233
        _Dec16std_z[i][m] = _Dec16std_z[i][m]*MASS*0.02233
        
        DEC18_sub_z[i][m] = DEC18_sub_z[i][m]*MASS*0.02233
        _Dec18std_z[i][m] = _Dec18std_z[i][m]*MASS*0.02233
        
        DEC14F_sub_z[i][m] = DEC14F_sub_z[i][m]*MASS*0.02233
        _Dec14Fstd_z[i][m] = _Dec14Fstd_z[i][m]*MASS*0.02233
        
        DEC16F_sub_z[i][m] = DEC16F_sub_z[i][m]*MASS*0.02233
        _Dec16Fstd_z[i][m] = _Dec16Fstd_z[i][m]*MASS*0.02233
        
        DEC18F_sub_z[i][m] = DEC18F_sub_z[i][m]*MASS*0.02233
        _Dec18Fstd_z[i][m] = _Dec18Fstd_z[i][m]*MASS*0.02233
    
    totals14 = []
    totals16 = []
    totals18 = []
    
    totals14F = []
    totals16F = []
    totals18F = []
    
    ERR = []
    ERRF = []

    for i in range(9):
        
        totals14.append( DEC14_sub_z[i][m] )
        totals14F.append( DEC14F_sub_z[i][m] )
    
        totals16.append( DEC16_sub_z[i][m] )
        totals16F.append( DEC16F_sub_z[i][m] )
    
        totals18.append( DEC18_sub_z[i][m] )
        totals18F.append( DEC18F_sub_z[i][m] )
        
        ERR.append( [_Dec14std_z[i][m], _Dec16std_z[i][m], _Dec18std_z[i][m]] )
        ERRF.append( [_Dec14Fstd_z[i][m], _Dec16Fstd_z[i][m], _Dec18Fstd_z[i][m]] )
    
    Av = [stat.median(totals14), stat.median(totals16), stat.median(totals18)]
    AvF = [stat.median(totals14F), stat.median(totals16F), stat.median(totals18F)]

    locations = ['1', '2', '3', '4', '5', '6', 'Obs.N.', 'Roof1', 'Roof2']
    mark = ['o', 'X', '*', 'd', 'D', 's', 'v', '<', '>']
    # colour = ['brown', 'black', 'blue',
    #           'yellow', 'green', 'red',
    #           'orange', 'pink', 'purple']
    DATE = ['14-12-2019', '16-12-2019', '18-12-2019']
    x = np.arange(1.5,8, 3)
    
    fig = plt.figure(figsize=(25,20))
    
    for p in range(len(locations)):
        tots_data = [totals14[p], totals16[p], totals18[p]]
    #     plt.errorbar(x, tots_data, yerr=ERR[p], fmt='o-', label='{}'.format(locations[p]), linewidth=2) #, alpha=0.1*(p+1))
        plt.scatter(x, tots_data, marker=mark[p], c='black',
                          s=400, label='{}'.format(locations[p]), alpha=0.4,)
        plt.plot(np.arange(1,8, 3), Av, '--', color='black', linewidth=1)
    for p in range(len(locations)):
        totsF_data = [totals14F[p], totals16F[p], totals18F[p]]
    #     plt.errorbar(x, totsF_data, yerr=ERRF[p], fmt='--', label='{}'.format(locations[p])) #, alpha=0.1*(p+1))
        plt.scatter(x, totsF_data, marker=mark[p], c='dodgerblue',
                          s=400, alpha=0.4) #, label='{}'.format(locations[p]),)
        plt.plot(np.arange(2,9, 3), AvF, '--', color='black',linewidth=1)
    bp0 = plt.boxplot([totals14, [], totals16, [], totals18,], positions=[1,3,4,6,7])
    bp1 = plt.boxplot([totals14F, [], totals16F, [], totals18F], positions=[2,3,5,6,8])
    # bp1 = plt.boxplot([[], [], [], [], []], positions=[2,3,5,6,8])
    for box in bp1['boxes']:
        box.set(color='dodgerblue', linewidth=2, alpha=0.5)
    plt.title('{} m/z'.format(MASS), fontsize=45)
    plt.ylabel('ng/ml', size=40)
    plt.xlabel('Date [DD-MM-YYYY]', size=40)
    plt.xticks(np.arange(1.5,8, 3), DATE)
    plt.text(8.6, 0, 'unfiltered\n', fontsize=30, bbox=dict(facecolor='grey', alpha=0.4) )
    plt.text(8.6, 0, '  filtered  ', fontsize=30, bbox=dict(facecolor='dodgerblue', alpha=0.4))
    plt.legend(loc='upper left', bbox_to_anchor=(1, 0.55), fontsize=35)
    
    fig.tight_layout()

    plt.savefig('{}.png'.format(MASS), bbox_inches='tight')
    
    print('plot for {} (indx: {}) saved.'.format(MASS, m)) #!!!
    
    plt.close() #!!!









#%% Spectrtal Plots

# ## input
# _DATA = DEC14_sub_z[8]
# _INDX = DEC14_sub[8].index
# _LOD = blnk_LOD
# _ERR = _Dec14std_z[8]
# _AXIS = np.arange(_DATA.size)

# ## plot
# plt.figure()
# plt.bar(_AXIS, _DATA, yerr=_ERR, label='Signal')
# # plt.plot(_AXIS, _DATA, label='Signal')
# plt.plot(_AXIS, _LOD, 'r--', label=r'LOD ($3\sigma$)')
# # plt.xticks(_AXIS, _INDX)
# plt.xlabel('m/z', size=40)
# plt.ylabel('Signal [ppb]', size=40)
# plt.title('Average PPB during TD', size=50)
# # plt.legend()
# # plt.grid()


