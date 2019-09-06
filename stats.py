#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 09:39:11 2019

@author: admin
"""

import numpy as np
import scipy.stats

def mean(x:'array')->float:
    return np.nanmean(x)

def median(x:'array')->float:
    return np.nanmedian(x)

def std(x:'array')->float:
    return np.nanstd(x)

def min(x:'array')->float:
    return np.nanmin(x)

def max(x:'array')->float:
    return np.nanmax(x)

def skew(x:'array')->float:
    return scipy.stats.skew(x)

def kurtosis(x:'array')->float:
    return scipy.stats.kurtosis(x)

def percentile(x:'array', p:float)->float:
    return np.nanpercentile(x, p)