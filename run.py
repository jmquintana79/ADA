#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Juan Quintana
@date: Thu Dec 26 08:41:29 2019
@email: juan.quintana@infiniamobile.com
"""

from functions import load_scikit_dataset
from classes import ADA
import numpy as np
import math



## load data
df = load_scikit_dataset()      
print('data: %s / %s'%(df.shape, df.columns))



## initialize
ada = ADA(df)

# numeric column
data = ada.get_data('SepalLengthCm')
# plot hist

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots()
# Sturge’s Rule
nbins = int(round(1 + 3.322 * np.log10(len(data))))


import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.signal import argrelextrema

def steps_estimation(df, col, threshold_freq = 0.0001, verbose = False):
    import matplotlib.pyplot as plt
    ## histogram density estimation with kde 
    noise = df[col].copy().dropna().values
    density = stats.gaussian_kde(noise)
    n, x = np.histogram(noise, bins = 250 , density=True)
    np.histogram(noise, bins = 250 , density=True)
    ## local maxima (histogram peaks) estimation = steps values
    imaxi = argrelextrema(density(x), np.greater)
    # validate if all peaks are zero
    is_all_zeros = len(np.where(n[imaxi]<=threshold_freq)[0])==len(n[imaxi])
    if is_all_zeros: threshold_freq = -9999.
    # select peaks = steps values average
    if verbose: print(imaxi, x[imaxi], n[imaxi], is_all_zeros)
    steps_avg = x[imaxi[0][np.where(n[imaxi]>threshold_freq)[0]]]
    print('step avg:',steps_avg)
    ## inpute for each value a step
    df['step_avg'] = df[col].apply(lambda x: impute_step_avg(x, steps_avg))
    
    """
    ## remove single spikes using WEEKLY resample
    step_avg = df[['step_avg']].resample('W').median()
    step_avg['year'] = [i.year for i in step_avg.index.tolist()]
    step_avg['week'] = [int(i.strftime("%W")) for i in step_avg.index.tolist()]
    ## fill modified step avg values: weekly to hourly
    dstep_avg = step_avg.reset_index(drop=True).set_index(['year', 'week']).to_dict()['step_avg']
    df['year'] = [i.year for i in df.index.tolist()]
    df['week'] = [int(i.strftime("%W")) for i in df.index.tolist()]
    df['step_avg_modif'] = df[['year','week', 'step_avg']].apply(lambda x: dstep_avg[(x[0],x[1])] if (x[0],x[1]) in dstep_avg else x[2], axis = 1)
    """
    
    ## remove single spikes using DAY OF YEAR resample
    step_avg = df[['step_avg']].resample('D').median()
    step_avg['year'] = [i.year for i in step_avg.index.tolist()]
    step_avg['doy'] = [int(i.strftime("%j")) for i in step_avg.index.tolist()]
    ## fill modified step avg values: weekly to hourly
    dstep_avg = step_avg.reset_index(drop=True).set_index(['year', 'doy']).to_dict()['step_avg']
    df['year'] = [i.year for i in df.index.tolist()]
    df['doy'] = [int(i.strftime("%j")) for i in df.index.tolist()]
    df['step_avg_modif'] = df[['year', 'doy', 'step_avg']].apply(lambda x: dstep_avg[(x[0],x[1])] if (x[0],x[1]) in dstep_avg else x[2], axis = 1)   
    
    
    ## categorize step_avg_modified
    dcat_step_avg_modif = dict()
    for ii, iv in enumerate(df.step_avg_modif.unique()): dcat_step_avg_modif[iv] = ii
    df['cat_step_avg_modif'] = df['step_avg_modif'].apply(lambda x: np.nan if np.isnan(x) else dcat_step_avg_modif[x])
    df.dropna(inplace = True)
    # plot
    if verbose:
        import matplotlib.pyplot as plt
        fig= plt.figure(figsize=(20,3))
        ax1 = plt.subplot2grid((1,4),(0,0),colspan=1)
        ax1.hist(noise, bins = 250 , density=True)
        # , title = 'peaks in: %s'%steps_avg
        ax1.plot(x, density(x))
        ax2 = plt.subplot2grid((1,4),(0,1),colspan=3)
        df[['step_avg', 'step_avg_modif']].plot( ax = ax2)
        plt.show()
    # return
    return df
