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
data = ada.get_data('PetalWidthCm')
# plot hist

#import matplotlib.pyplot as plt
#fig, ax = plt.subplots()




import scipy.stats as stats
from scipy.signal import argrelextrema
threshold_freq = 0.0001

## histogram density estimation with kde 
noise = data[~np.isnan(data)]
density = stats.gaussian_kde(noise)
n, x = np.histogram(noise, bins = 250 , density=True)

## local maxima (histogram peaks) estimation = steps values
imaxi = argrelextrema(density(x), np.greater)
# validate if all peaks are zero
is_all_zeros = len(np.where(n[imaxi]<=threshold_freq)[0])==len(n[imaxi])
if is_all_zeros: threshold_freq = -9999.
# select peaks = steps values average
steps_avg = x[imaxi[0][np.where(n[imaxi]>threshold_freq)[0]]]
print('step avg:',steps_avg)

# %%

import matplotlib.pyplot as plt
fig, ax1 = plt.subplots()
ax1.hist(noise, bins='auto' , density=False, histtype='stepfilled', alpha=0.2)
ax2 = ax1.twinx()
ax2.plot(x, density(x))
fig.tight_layout()
plt.show()

